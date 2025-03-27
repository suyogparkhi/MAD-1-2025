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