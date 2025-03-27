from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired
from models.chapter import Chapter

class QuizForm(FlaskForm):
    chapter_id = SelectField('Chapter', coerce=int, validators=[DataRequired()])
    date_of_quiz = DateField('Date of Quiz', format='%Y-%m-%d', validators=[DataRequired()])
    time_duration = StringField('Duration (e.g., "30 minutes")', validators=[DataRequired()])
    remarks = TextAreaField('Remarks')
    
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        # If a subject_id is provided, filter chapters by that subject
        if 'subject_id' in kwargs:
            subject_id = kwargs.pop('subject_id')
            self.chapter_id.choices = [(c.id, c.name) for c in Chapter.query.filter_by(subject_id=subject_id).all()]
        else:
            # Otherwise, show all chapters with subject name
            self.chapter_id.choices = [(c.id, f"{c.subject.name} - {c.name}") 
                                      for c in Chapter.query.join(Chapter.subject).all()] 