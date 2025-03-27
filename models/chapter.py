from models import db

class Chapter(db.Model):
    __tablename__ = 'chapters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (db.UniqueConstraint('name', 'subject_id', name='unique_chapter_per_subject'),)
    
    def __repr__(self):
        return f'<Chapter: {self.name}>' 