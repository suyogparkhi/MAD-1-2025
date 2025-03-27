from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from models import db
from models.user import User
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question
from models.score import Score
from forms.subject_forms import SubjectForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    # Get counts for dashboard
    users_count = User.query.filter_by(role='user').count()
    subjects_count = Subject.query.count()
    chapters_count = Chapter.query.count()
    quizzes_count = Quiz.query.count()
    questions_count = Question.query.count()
    attempts_count = Score.query.count()
    
    # Get recent scores
    recent_scores = Score.query.order_by(Score.time_stamp_of_attempt.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                          users_count=users_count,
                          subjects_count=subjects_count,
                          chapters_count=chapters_count,
                          quizzes_count=quizzes_count,
                          questions_count=questions_count,
                          attempts_count=attempts_count,
                          recent_scores=recent_scores,
                          title='Admin Dashboard')

# Subject routes
@admin_bp.route('/subjects')
@login_required
@admin_required
def subjects():
    subjects = Subject.query.all()
    return render_template('admin/subjects/index.html', subjects=subjects, title='Subjects')

@admin_bp.route('/subjects/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject created successfully!', 'success')
        return redirect(url_for('admin.subjects'))
    
    return render_template('admin/subjects/create.html', form=form, title='Create Subject')

@admin_bp.route('/subjects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    form = SubjectForm(obj=subject)
    form.subject_id = id  # Set to check in validation
    
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin.subjects'))
    
    return render_template('admin/subjects/edit.html', form=form, subject=subject, title='Edit Subject')

@admin_bp.route('/subjects/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('admin.subjects')) 