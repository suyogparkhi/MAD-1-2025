from models import db
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    time_duration = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.Text)
    
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quiz: ID {self.id} - Chapter {self.chapter_id}>'
    
    @property
    def total_questions(self):
        return len(self.questions) 