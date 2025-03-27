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