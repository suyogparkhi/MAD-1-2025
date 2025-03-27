from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from models.subject import Subject

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    
    def validate_name(self, field):
        # Check if the subject name already exists when creating a new subject
        if not hasattr(self, 'subject_id'):
            subject = Subject.query.filter_by(name=field.data).first()
            if subject:
                raise ValidationError('A subject with this name already exists.') 