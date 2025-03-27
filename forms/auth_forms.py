from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models.user import User

class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired()])
    qualification = StringField('Qualification')
    dob = DateField('Date of Birth', format='%Y-%m-%d')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.') 