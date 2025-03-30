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
from forms.chapter_forms import ChapterForm
from forms.quiz_forms import QuizForm
from forms.question_forms import QuestionForm
from datetime import datetime, timedelta

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
    
    # Get subjects for performance summary
    subjects = Subject.query.all()
    
    # Calculate subject attempt counts and average scores
    subject_attempts = {}
    subject_avg_scores = {}
    
    for subject in subjects:
        # Get chapters in this subject
        chapter_ids = [chapter.id for chapter in subject.chapters]
        
        # Get quizzes in these chapters
        quiz_ids = []
        for chapter_id in chapter_ids:
            chapter_quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
            quiz_ids.extend([quiz.id for quiz in chapter_quizzes])
        
        # Get scores for these quizzes
        attempts = Score.query.filter(Score.quiz_id.in_(quiz_ids)).count() if quiz_ids else 0
        subject_attempts[subject.id] = attempts
        
        # Calculate average score percentage
        if attempts > 0:
            scores = Score.query.filter(Score.quiz_id.in_(quiz_ids)).all()
            total_percentage = 0
            for score in scores:
                quiz = Quiz.query.get(score.quiz_id)
                if quiz and quiz.total_questions > 0:  # Avoid division by zero
                    percentage = (score.total_scored / quiz.total_questions) * 100
                    total_percentage += percentage
            subject_avg_scores[subject.id] = total_percentage / attempts if attempts > 0 else 0
        else:
            subject_avg_scores[subject.id] = 0
    
    # Calculate score distribution for chart
    score_ranges = [0, 0, 0, 0]  # [0-39%, 40-59%, 60-79%, 80-100%]
    
    all_scores = Score.query.all()
    for score in all_scores:
        quiz = Quiz.query.get(score.quiz_id)
        if quiz and quiz.total_questions > 0:  # Avoid division by zero
            percentage = (score.total_scored / quiz.total_questions) * 100
            if percentage < 40:
                score_ranges[0] += 1
            elif percentage < 60:
                score_ranges[1] += 1
            elif percentage < 80:
                score_ranges[2] += 1
            else:
                score_ranges[3] += 1
    
    # Calculate daily activity for the past 7 days
    daily_attempts = [0] * 7
    today = datetime.utcnow().date()
    
    for i in range(7):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        count = Score.query.filter(
            Score.time_stamp_of_attempt >= day_start,
            Score.time_stamp_of_attempt <= day_end
        ).count()
        # Store in reverse order (for chart display)
        daily_attempts[6-i] = count
    
    return render_template('admin/dashboard.html',
                          users_count=users_count,
                          subjects_count=subjects_count,
                          chapters_count=chapters_count,
                          quizzes_count=quizzes_count,
                          questions_count=questions_count,
                          attempts_count=attempts_count,
                          recent_scores=recent_scores,
                          subjects=subjects,
                          subject_attempts=subject_attempts,
                          subject_avg_scores=subject_avg_scores,
                          score_ranges=score_ranges,
                          daily_attempts=daily_attempts,
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

# Chapter routes
@admin_bp.route('/subjects/<int:subject_id>/chapters')
@login_required
@admin_required
def chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return render_template('admin/chapters/index.html', 
                          subject=subject, 
                          chapters=chapters,
                          title=f'Chapters - {subject.name}')

@admin_bp.route('/subjects/<int:subject_id>/chapters/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = ChapterForm()
    
    # Preselect the subject
    form.subject_id.data = subject_id
    form.subject_id.choices = [(subject.id, subject.name)]
    
    if form.validate_on_submit():
        chapter = Chapter(
            name=form.name.data,
            description=form.description.data,
            subject_id=form.subject_id.data
        )
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter created successfully!', 'success')
        return redirect(url_for('admin.chapters', subject_id=subject_id))
    
    return render_template('admin/chapters/create.html', 
                          form=form, 
                          subject=subject,
                          title=f'Create Chapter - {subject.name}')

@admin_bp.route('/chapters/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    form = ChapterForm(obj=chapter)
    form.chapter_id = id  # Set to check in validation
    
    if form.validate_on_submit():
        chapter.name = form.name.data
        chapter.description = form.description.data
        chapter.subject_id = form.subject_id.data
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('admin.chapters', subject_id=chapter.subject_id))
    
    return render_template('admin/chapters/edit.html', 
                          form=form, 
                          chapter=chapter,
                          title=f'Edit Chapter - {chapter.name}')

@admin_bp.route('/chapters/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    subject_id = chapter.subject_id
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted successfully!', 'success')
    return redirect(url_for('admin.chapters', subject_id=subject_id))

# Quiz routes
@admin_bp.route('/chapters/<int:chapter_id>/quizzes')
@login_required
@admin_required
def quizzes(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return render_template('admin/quizzes/index.html', 
                          chapter=chapter, 
                          quizzes=quizzes,
                          title=f'Quizzes - {chapter.name}')

@admin_bp.route('/chapters/<int:chapter_id>/quizzes/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    form = QuizForm()
    
    if form.validate_on_submit():
        quiz = Quiz(
            date_of_quiz=form.date_of_quiz.data,
            time_duration=form.time_duration.data,
            remarks=form.remarks.data,
            chapter_id=chapter_id
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('admin.quizzes', chapter_id=chapter_id))
    
    return render_template('admin/quizzes/create.html', 
                          form=form, 
                          chapter=chapter,
                          title=f'Create Quiz - {chapter.name}')

@admin_bp.route('/quizzes/<int:quiz_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizForm(obj=quiz)
    
    if form.validate_on_submit():
        quiz.date_of_quiz = form.date_of_quiz.data
        quiz.time_duration = form.time_duration.data
        quiz.remarks = form.remarks.data
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('admin.quizzes', chapter_id=quiz.chapter_id))
    
    return render_template('admin/quizzes/edit.html', 
                          form=form, 
                          quiz=quiz,
                          title=f'Edit Quiz')

@admin_bp.route('/quizzes/<int:quiz_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('admin.quizzes', chapter_id=chapter_id))

# Question routes
@admin_bp.route('/quizzes/<int:quiz_id>/questions')
@login_required
@admin_required
def questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('admin/questions/index.html', 
                          quiz=quiz, 
                          questions=questions,
                          title=f'Questions - {quiz.chapter.name} Quiz')

@admin_bp.route('/quizzes/<int:quiz_id>/questions/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    
    if form.validate_on_submit():
        # Create the question using the actual database schema fields
        question = Question(
            quiz_id=quiz_id,
            question_statement=form.question_text.data,
            option1=form.option_a.data or "",
            option2=form.option_b.data or "",
            option3=form.option_c.data or "",
            option4=form.option_d.data or "",
            correct_answer=1  # Default value
        )
        
        # Set correct answer based on question type
        if form.question_type.data == 'multiple_choice':
            if form.correct_option.data == 'a':
                question.correct_answer = 1
            elif form.correct_option.data == 'b':
                question.correct_answer = 2
            elif form.correct_option.data == 'c':
                question.correct_answer = 3
            elif form.correct_option.data == 'd':
                question.correct_answer = 4
        elif form.question_type.data == 'true_false':
            # For true/false, use option1 as 'True' and option2 as 'False'
            question.option1 = "True"
            question.option2 = "False"
            question.option3 = ""
            question.option4 = ""
            question.correct_answer = 1 if form.correct_boolean.data == 'true' else 2
        else:  # short_answer - use option1 as the correct answer
            question.option1 = form.correct_answer.data or ""
            question.option2 = ""
            question.option3 = ""
            question.option4 = ""
            question.correct_answer = 1
        
        db.session.add(question)
        db.session.commit()
        flash('Question created successfully!', 'success')
        return redirect(url_for('admin.questions', quiz_id=quiz_id))
    
    return render_template('admin/questions/create.html', 
                          form=form, 
                          quiz=quiz,
                          title=f'Create Question')

@admin_bp.route('/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Determine question type and populate form accordingly
    question_type = 'multiple_choice'  # Default
    
    # True/False check
    if question.option1 == "True" and question.option2 == "False" and not question.option3 and not question.option4:
        question_type = 'true_false'
    # Short answer check
    elif question.option2 == "" and question.option3 == "" and question.option4 == "":
        question_type = 'short_answer'
    
    # Create form and populate it
    form = QuestionForm(
        question_text=question.question_statement,
        question_type=question_type,
        difficulty='medium',  # Default since the original model doesn't have this
        marks=1  # Default since the original model doesn't have this
    )
    
    # Set form fields based on question type
    if question_type == 'multiple_choice':
        form.option_a.data = question.option1
        form.option_b.data = question.option2
        form.option_c.data = question.option3
        form.option_d.data = question.option4
        
        # Set correct option
        if question.correct_answer == 1:
            form.correct_option.data = 'a'
        elif question.correct_answer == 2:
            form.correct_option.data = 'b'
        elif question.correct_answer == 3:
            form.correct_option.data = 'c'
        elif question.correct_answer == 4:
            form.correct_option.data = 'd'
    elif question_type == 'true_false':
        form.correct_boolean.data = 'true' if question.correct_answer == 1 else 'false'
    else:  # short_answer
        form.correct_answer.data = question.option1
    
    if form.validate_on_submit():
        # Update the question with existing schema fields
        question.question_statement = form.question_text.data
        
        if form.question_type.data == 'multiple_choice':
            question.option1 = form.option_a.data or ""
            question.option2 = form.option_b.data or ""
            question.option3 = form.option_c.data or ""
            question.option4 = form.option_d.data or ""
            
            # Set correct answer based on selected option
            if form.correct_option.data == 'a':
                question.correct_answer = 1
            elif form.correct_option.data == 'b':
                question.correct_answer = 2
            elif form.correct_option.data == 'c':
                question.correct_answer = 3
            elif form.correct_option.data == 'd':
                question.correct_answer = 4
            else:
                question.correct_answer = 1  # Default to option 1
        elif form.question_type.data == 'true_false':
            # For true/false, use option1 as 'True' and option2 as 'False'
            question.option1 = "True"
            question.option2 = "False"
            question.option3 = ""
            question.option4 = ""
            question.correct_answer = 1 if form.correct_boolean.data == 'true' else 2
        else:  # short_answer - use option1 as the correct answer
            question.option1 = form.correct_answer.data or ""
            question.option2 = ""
            question.option3 = ""
            question.option4 = ""
            question.correct_answer = 1
        
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('admin.questions', quiz_id=question.quiz_id))
    
    return render_template('admin/questions/edit.html', 
                          form=form, 
                          question=question,
                          title=f'Edit Question')

@admin_bp.route('/questions/<int:question_id>/delete')
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('admin.questions', quiz_id=quiz_id)) 