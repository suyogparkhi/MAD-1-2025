from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class QuizForm(FlaskForm):
    date_of_quiz = DateField('Quiz Date', validators=[DataRequired()])
    time_duration = StringField('Time Duration', validators=[DataRequired(), Length(max=50)], 
                              description="Enter the duration in minutes (e.g., 30 minutes)")
    remarks = TextAreaField('Remarks', validators=[Optional(), Length(max=500)],
                          description="Optional notes about this quiz")
    submit = SubmitField('Save Quiz') 