# Quiz Master V1 - Comprehensive Development Plan

This development plan provides step-by-step instructions for implementing the Quiz Master V1 application per the project requirements. Following this plan will ensure all core functionalities are implemented correctly.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Database Design](#database-design)
4. [Project Structure](#project-structure)
5. [Implementation Steps](#implementation-steps)
6. [Testing Plan](#testing-plan)
7. [Deployment Instructions](#deployment-instructions)

## Project Overview

Quiz Master V1 is a multi-user web application for exam preparation across multiple courses. The application has two user roles:
- **Admin (Quiz Master)**: Manages users, subjects, chapters, and quizzes
- **Users**: Register, login, attempt quizzes, and view their results

The application follows a hierarchical structure:
- Subjects contain multiple Chapters
- Chapters contain multiple Quizzes
- Quizzes contain multiple Questions
- Users can attempt Quizzes and receive Scores

## Technology Stack

As specified in the requirements, the application will use:
- **Backend**: Flask
- **Frontend**: Jinja2 templates, HTML, CSS, Bootstrap
- **Database**: SQLite
- **Additional Libraries**: Flask-Login, Flask-WTF, Chart.js (optional for charts)

## Database Design

### Entity-Relationship Diagram

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Users   │    │ Subjects │    │ Chapters │    │  Quizzes │    │Questions │
├──────────┤    ├──────────┤    ├──────────┤    ├──────────┤    ├──────────┤
│id        │    │id        │    │id        │    │id        │    │id        │
│username  │    │name      │    │name      │    │chapter_id│    │quiz_id   │
│password  │    │description   │description│    │date      │    │statement │
│full_name │    └──────────┘    │subject_id│    │duration  │    │option1   │
│qualification     │            └──────────┘    │remarks   │    │option2   │
│dob       │                        │           └──────────┘    │option3   │
│role      │                        │                │          │option4   │
└──────────┘                        │                │          │correct_answer│
      │                             │                │          └──────────┘
      │                             │                │
      │                             │                │
      └─────────────────────────────┼────────────────┼──────┐
                                    │                │      │
                                    │                │      │
                                ┌───┴────┐       ┌───┴────┐ │
                                │ Scores │       │Attempts│ │
                                ├────────┤       ├────────┤ │
                                │id      │       │id      │ │
                                │user_id │───────│user_id │ │
                                │quiz_id │       │quiz_id │ │
                                │timestamp       │timestamp  │
                                │total_score     │completed│ │
                                └────────┘       └────────┘ │
                                                            │
                                                            │
```

### Database Schema

Create the following tables in SQLite:

1. **Users Table**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    qualification TEXT,
    dob DATE,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'user'))
);
```

2. **Subjects Table**
```sql
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);
```

3. **Chapters Table**
```sql
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    subject_id INTEGER NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
    UNIQUE (name, subject_id)
);
```

4. **Quizzes Table**
```sql
CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    date_of_quiz DATE NOT NULL,
    time_duration TEXT NOT NULL,
    remarks TEXT,
    FOREIGN KEY (chapter_id) REFERENCES chapters (id) ON DELETE CASCADE
);
```

5. **Questions Table**
```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    question_statement TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_answer INTEGER NOT NULL CHECK (correct_answer BETWEEN 1 AND 4),
    FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE
);
```

6. **Scores Table**
```sql
CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    time_stamp_of_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_scored INTEGER NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

## Project Structure

Here's the folder structure for the Quiz Master V1 application:

```
quiz_master_v1/
├── app.py                  # Main application file
├── config.py               # Configuration settings
├── requirements.txt        # Dependencies
├── models/
│   ├── __init__.py         # Initialize the database
│   ├── user.py             # User model
│   ├── subject.py          # Subject model
│   ├── chapter.py          # Chapter model
│   ├── quiz.py             # Quiz model
│   ├── question.py         # Question model
│   └── score.py            # Score model
├── controllers/
│   ├── __init__.py
│   ├── auth.py             # Authentication controllers
│   ├── admin.py            # Admin controllers
│   ├── user.py             # User controllers
│   └── api.py              # API endpoints (optional)
├── forms/
│   ├── __init__.py
│   ├── auth_forms.py       # Login/Register forms
│   ├── subject_forms.py    # Subject CRUD forms
│   ├── chapter_forms.py    # Chapter CRUD forms
│   ├── quiz_forms.py       # Quiz CRUD forms
│   └── question_forms.py   # Question CRUD forms
├── static/
│   ├── css/
│   │   └── styles.css      # Custom CSS
│   ├── js/
│   │   ├── charts.js       # Chart.js integration
│   │   └── quiz.js         # Quiz timer and validation
│   └── img/
├── templates/
│   ├── layout.html         # Base template
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── subjects/
│   │   │   ├── index.html
│   │   │   ├── create.html
│   │   │   └── edit.html
│   │   ├── chapters/
│   │   │   ├── index.html
│   │   │   ├── create.html
│   │   │   └── edit.html
│   │   ├── quizzes/
│   │   │   ├── index.html
│   │   │   ├── create.html
│   │   │   └── edit.html
│   │   └── questions/
│   │       ├── index.html
│   │       ├── create.html
│   │       └── edit.html
│   └── user/
│       ├── dashboard.html
│       ├── subjects.html
│       ├── chapters.html
│       ├── quizzes.html
│       ├── take_quiz.html
│       └── results.html
└── instance/
    └── quiz_master.db      # SQLite database file
```

## Implementation Steps

Follow these steps in sequence to implement the Quiz Master V1 application:

### 1. Project Setup

1. Create a new Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install flask flask-login flask-wtf email_validator
```

3. Create requirements.txt:
```bash
pip freeze > requirements.txt
```

4. Create the initial project structure:
```bash
mkdir -p quiz_master_v1/{models,controllers,forms,static/{css,js,img},templates/{auth,admin/{subjects,chapters,quizzes,questions},user},instance}
touch quiz_master_v1/app.py quiz_master_v1/config.py
```

### 2. Database Models Implementation

1. Create the models with proper relationships:

**models/__init__.py**
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Create admin user if not exists
        from models.user import User
        admin = User.query.filter_by(username='admin@example.com').first()
        if not admin:
            from werkzeug.security import generate_password_hash
            admin = User(
                username='admin@example.com',
                password=generate_password_hash('admin123'),
                full_name='Administrator',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
```

**models/user.py**
```python
from models import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)
    role = db.Column(db.String(10), default='user')
    
    scores = db.relationship('Score', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def is_admin(self):
        return self.role == 'admin'
```

Continue implementing models for Subject, Chapter, Quiz, Question, and Score classes following the schema defined above.

### 3. Authentication System

1. Implement Flask-Login setup in app.py.
2. Create login and registration forms.
3. Implement authentication routes and templates.

### 4. Admin Features

1. Implement CRUD operations for subjects, chapters, quizzes, and questions.
2. Create admin dashboard with summary charts.
3. Implement user search functionality.

### 5. User Features

1. Implement user dashboard.
2. Create quiz taking functionality with timer.
3. Implement quiz results and history display.

### 6. Charts and Visualizations

1. Integrate Chart.js for summary charts.
2. Implement data aggregation for charts.

### 7. API Endpoints (Optional)

1. Create RESTful API endpoints for subjects, chapters, and quizzes.

## Detailed Implementation

### App Configuration (app.py)

```python
from flask import Flask, render_template
from flask_login import LoginManager
from models import init_db
from models.user import User
import os

# Import controllers
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.user import user_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Configure the application
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "quiz_master.db")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Initialize the database
    init_db(app)
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    
    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

### Authentication Controller (controllers/auth.py)

```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db
from models.user import User
from forms.auth_forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if user.is_admin():
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('user.dashboard'))
        flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            full_name=form.full_name.data,
            qualification=form.qualification.data,
            dob=form.dob.data,
            role='user'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
```

### Admin Controller (controllers/admin.py)

```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from models import db
from models.user import User
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question
from forms.subject_forms import SubjectForm
from forms.chapter_forms import ChapterForm
from forms.quiz_forms import QuizForm
from forms.question_forms import QuestionForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    # Get counts for dashboard
    users_count = User.query.filter_by(role='user').count()
    subjects_count = Subject.query.count()
    chapters_count = Chapter.query.count()
    quizzes_count = Quiz.query.count()
    
    return render_template('admin/dashboard.html',
                          users_count=users_count,
                          subjects_count=subjects_count,
                          chapters_count=chapters_count,
                          quizzes_count=quizzes_count)

# Subject routes
@admin_bp.route('/subjects')
@login_required
@admin_required
def subjects():
    subjects = Subject.query.all()
    return render_template('admin/subjects/index.html', subjects=subjects)

@admin_bp.route('/subjects/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject created successfully!', 'success')
        return redirect(url_for('admin.subjects'))
    
    return render_template('admin/subjects/create.html', form=form)

# Implement similar routes for chapters, quizzes, and questions
```

Continue implementing remaining controllers for user dashboard and quiz-taking functionality.

## Forms Implementation

Create WTForms classes for all CRUD operations:

**forms/auth_forms.py**
```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired()])
    qualification = StringField('Qualification')
    dob = DateField('Date of Birth', format='%Y-%m-%d')
```

## Templates Implementation

1. Create base template with Bootstrap:

**templates/layout.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Quiz Master{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    {% block styles %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">Quiz Master</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    {% if current_user.is_authenticated %}
                        {% if current_user.is_admin() %}
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('admin.dashboard') }}">Dashboard</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('admin.subjects') }}">Subjects</a>
                            </li>
                            <!-- More admin navigation items -->
                        {% else %}
                            <li class="nav-item">
                                <a class="nav-link" href="{{ url_for('user.dashboard') }}">Dashboard</a>
                            </li>
                            <!-- More user navigation items -->
                        {% endif %}
                    {% endif %}
                </ul>
                <ul class="navbar-nav">
                    {% if current_user.is_authenticated %}
                        <li class="nav-item">
                            <span class="nav-link">Welcome, {{ current_user.full_name }}</span>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('auth.logout') }}">Logout</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('auth.login') }}">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('auth.register') }}">Register</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <footer class="bg-light py-4 mt-5">
        <div class="container text-center">
            <p>&copy; 2025 Quiz Master</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="{{ url_for('static', filename='js/charts.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

Create similar templates for all views.

## Testing Plan

1. **Unit Tests**
   - Test database models
   - Test form validation
   - Test authentication functionality

2. **Integration Tests**
   - Test admin dashboard functionality
   - Test subject/chapter/quiz/question CRUD operations
   - Test quiz taking functionality

3. **User Acceptance Testing**
   - Test the complete user journey
   - Test responsive design

## Deployment Instructions

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
flask --app app.py init-db
```

3. Run the application:
```bash
flask --app app.py run
```

## Additional Notes

1. Ensure all form submissions include CSRF protection
2. Validate all user input on both client and server sides
3. Follow RESTful design principles for API endpoints
4. Use appropriate status codes and error handling
5. Add proper documentation and comments throughout the code
6. Use meaningful variable and function names

By following this development plan, you will create a fully functional Quiz Master V1 application that meets all the project requirements.
