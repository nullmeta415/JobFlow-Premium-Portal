from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from models import db, User, Job

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SECRET_KEY'] = 'dev-key-123'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

# --- SECURE ADMIN LOGIC ---

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'Admin'
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class UserAdminView(SecureModelView):
    """Custom view for User management to ensure secure password hashing."""
    form_choices = {'role': [('Admin', 'Admin'), ('Employer', 'Employer'), ('Seeker', 'Job Seeker')]}
    def on_model_change(self, form, model, is_created):
        if form.password.data and not form.password.data.startswith(('scrypt', 'pbkdf2')):
            model.password = generate_password_hash(form.password.data, method='scrypt')

class MyAdminIndexView(AdminIndexView):
    """Admin Dashboard with real-time statistics."""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'Admin'
    @expose('/')
    def index(self):
        stats = {
            'user_count': User.query.count(),
            'job_count': Job.query.count(),
            'employer_count': User.query.filter_by(role='Employer').count(),
            'seeker_count': User.query.filter_by(role='Seeker').count()
        }
        return self.render('admin/index.html', **stats)

admin = Admin(app, name='JobFlow Admin', index_view=MyAdminIndexView(template='admin/index.html'))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(SecureModelView(Job, db.session))

# --- ROUTES ---

@app.route('/')
def index():
    all_jobs = Job.query.order_by(Job.id.desc()).all()
    return render_template('index.html', jobs=all_jobs)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form.get('email')).first():
            flash("Email already exists", "danger")
            return redirect(url_for('signup'))
        new_user = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            password=generate_password_hash(request.form.get('password'), method='scrypt'),
            role=request.form.get('role')
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        flash("Invalid Credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role != 'Employer':
        flash("Access denied.", "danger")
        return redirect(url_for('index'))
    if request.method == 'POST':
        new_job = Job(
            title=request.form.get('title'),
            company=request.form.get('company'),
            location=request.form.get('location'),
            salary=request.form.get('salary'),
            category=request.form.get('category'),
            description=request.form.get('description')
        )
        db.session.add(new_job)
        db.session.commit()
        flash("Job posted successfully!", "success")
        return redirect(url_for('index'))
    return render_template('post_job.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')  # Get the search term from the URL
    results = Job.query.filter(
        (Job.title.ilike(f'%{query}%')) | 
        (Job.company.ilike(f'%{query}%')) | 
        (Job.location.ilike(f'%{query}%'))
    ).all()
    
    # Pass 'query' to the template so we can display it in the 'No jobs' message
    return render_template('index.html', jobs=results, query=query)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/job/<int:job_id>')
def job_details(job_id):
    # Fetch the job by ID or return a 404 error if not found
    job = Job.query.get_or_404(job_id)
    return render_template('job_details.html', job=job)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role='Admin').first():
            db.session.add(User(username="admin", email="admin@jobflow.com", 
                                password=generate_password_hash("admin123", method='scrypt'), role="Admin"))
            db.session.commit()
    app.run(debug=True)