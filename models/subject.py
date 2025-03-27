from models import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject: {self.name}>' 