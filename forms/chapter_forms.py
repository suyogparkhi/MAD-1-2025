from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from models.chapter import Chapter
from models.subject import Subject

class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)
        self.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
    
    def validate_name(self, field):
        # Check if the chapter name already exists in the subject
        if hasattr(self, 'chapter_id') and self.chapter_id.data:
            # Skip validation if editing the same chapter
            chapter = Chapter.query.get(self.chapter_id.data)
            if chapter and chapter.name == field.data and chapter.subject_id == self.subject_id.data:
                return
                
        chapter = Chapter.query.filter_by(name=field.data, subject_id=self.subject_id.data).first()
        if chapter:
            raise ValidationError('A chapter with this name already exists in this subject.') 