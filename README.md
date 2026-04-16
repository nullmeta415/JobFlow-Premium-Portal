# JobFlow - Premium Job Portal 🚀

JobFlow is a full-stack, role-based career platform designed to connect employers with talent through a modern, high-performance interface. The application features a secure admin dashboard, dynamic job searching, and a refined user experience.

## ✨ Features

### 👤 For Job Seekers
- **Dynamic Search**: Filter jobs by title, company, or location with personalized query feedback.
- **Job Details**: View comprehensive job descriptions, salary ranges, and metadata before applying.
- **Profile Management**: A dedicated hub to manage account details and view application status.

### 🏢 For Employers
- **Job Posting**: A specialized dashboard to publish new listings with category and salary tagging.
- **Branded Cards**: Automated generation of premium job cards on the public homepage.

### 🛡️ For Admins (Secret Panel)
- **Real-Time Analytics**: Dashboard view showing total users, job counts, and role distributions.
- **Database Control**: Direct CRUD access to Users and Jobs.
- **Security**: Automated password hashing and role-based dropdown management within the panel.

## 🛠️ Technology Stack
- **Backend**: Python / Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login with Scrypt password hashing
- **UI/UX**: Bootstrap 5, Animate On Scroll (AOS), Glassmorphism CSS, and custom 3D animations
- **Admin**: Flask-Admin

## 🚀 Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install flask flask_sqlalchemy flask_login flask_admin werkzeug
   ```

2. **Initialize Database**:
   Run the application once to automatically generate the database schema and master admin account.
   ```bash
   python app.py
   ```

3. **Access the Application**:
   - Website: `http://127.0.0.1:5000`
   - Secret Admin Panel: `http://127.0.0.1:5000/admin`

## 🔑 Default Admin Credentials
- **Email**: `admin@jobflow.com`
- **Password**: `admin123`

## 🎨 UI Design Notes
The project utilizes a "Subtle Lift" animation logic for forms and profiles to ensure high usability, while maintaining 3D interactive elements on the homepage to attract user attention.
```
#flask #python #sqlite #job-portal #web-development #sqlalchemy #bootstrap5 #admin-dashboard #role-based-access