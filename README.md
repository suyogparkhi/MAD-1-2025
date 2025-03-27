# Quiz Master V1

Quiz Master is a multi-user web application designed for exam preparation across multiple courses. The application supports two user roles: administrators (Quiz Masters) and regular users.

## Features

### Admin Features
- User management
- Subject, chapter, and quiz management
- Question creation and editing
- View quiz statistics and user results

### User Features
- Register and login to the system
- Browse subjects and chapters
- Take quizzes with timed sessions
- View quiz results and history

## Technology Stack

- **Backend**: Flask
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Frontend**: Bootstrap 5, Jinja2 templates
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## Project Structure

The application follows a modular structure with separate components for models, controllers, forms, and templates.

```
quiz_master_v1/
├── app.py                  # Main application file
├── requirements.txt        # Dependencies
├── models/                 # Database models
├── controllers/            # Route controllers
├── forms/                  # Form definitions
├── static/                 # Static assets
│   ├── css/
│   ├── js/
│   └── img/
├── templates/              # Jinja2 templates
└── instance/               # Instance-specific data
    └── quiz_master.db      # SQLite database
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/<repo-name>
cd quiz-master-v1
```

2. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Access the application at `http://localhost:5000`

## Default Admin Account

- **Email**: admin@example.com
- **Password**: admin123

## Database Schema

- **Users**: Stores user information and credentials
- **Subjects**: Contains different subjects
- **Chapters**: Contains chapters within subjects
- **Quizzes**: Stores quizzes for each chapter
- **Questions**: Contains questions for each quiz
- **Scores**: Tracks user quiz attempts and scores

## License

MIT

## Contributors

- Your Name - Initial work 