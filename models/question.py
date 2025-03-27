from models import db

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (
        db.CheckConstraint('correct_answer BETWEEN 1 AND 4', name='check_correct_answer'),
    )
    
    def __repr__(self):
        return f'<Question: ID {self.id} - Quiz {self.quiz_id}>' 