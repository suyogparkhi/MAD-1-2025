from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class QuestionForm(FlaskForm):
    question_text = TextAreaField('Question Text', validators=[DataRequired(), Length(min=5, max=1000)])
    
    question_type = SelectField('Question Type', choices=[
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer')
    ], validators=[DataRequired()])
    
    difficulty = SelectField('Difficulty Level', choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ], validators=[DataRequired()])
    
    marks = IntegerField('Marks', validators=[DataRequired(), NumberRange(min=1, max=100)])
    
    # Multiple choice fields
    option_a = StringField('Option A', validators=[Optional(), Length(max=255)])
    option_b = StringField('Option B', validators=[Optional(), Length(max=255)])
    option_c = StringField('Option C', validators=[Optional(), Length(max=255)])
    option_d = StringField('Option D', validators=[Optional(), Length(max=255)])
    
    correct_option = SelectField('Correct Option', choices=[
        ('a', 'Option A'),
        ('b', 'Option B'),
        ('c', 'Option C'),
        ('d', 'Option D')
    ], validators=[Optional()])
    
    # True/False field
    correct_boolean = SelectField('Correct Answer', choices=[
        ('true', 'True'),
        ('false', 'False')
    ], validators=[Optional()])
    
    # Short answer field
    correct_answer = StringField('Correct Answer', validators=[Optional(), Length(max=255)]) 