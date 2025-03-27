from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    question_statement = TextAreaField('Question', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    correct_answer = RadioField('Correct Answer', choices=[
        ('1', 'Option 1'), 
        ('2', 'Option 2'), 
        ('3', 'Option 3'), 
        ('4', 'Option 4')
    ], validators=[DataRequired()], coerce=int) 