from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question
from models.score import Score
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
@login_required
def dashboard():
    # Get statistics for the user dashboard
    total_quizzes = Quiz.query.count()
    attempted_quizzes = Score.query.filter_by(user_id=current_user.id).count()
    subjects = Subject.query.all()
    
    # Get recent quiz attempts
    recent_scores = Score.query.filter_by(user_id=current_user.id) \
                          .order_by(Score.time_stamp_of_attempt.desc()) \
                          .limit(5).all()
    
    return render_template('user/dashboard.html',
                          total_quizzes=total_quizzes,
                          attempted_quizzes=attempted_quizzes,
                          subjects=subjects,
                          recent_scores=recent_scores,
                          title='Dashboard')

@user_bp.route('/subjects')
@login_required
def subjects():
    subjects = Subject.query.all()
    return render_template('user/subjects.html', subjects=subjects, title='Subjects')

@user_bp.route('/subjects/<int:subject_id>/chapters')
@login_required
def chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return render_template('user/chapters.html', 
                          subject=subject, 
                          chapters=chapters,
                          title=f'Chapters - {subject.name}')

@user_bp.route('/chapters/<int:chapter_id>/quizzes')
@login_required
def quizzes(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    # Mark quizzes that have been attempted by the user
    for quiz in quizzes:
        score = Score.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).first()
        quiz.attempted = score is not None
        quiz.score = score.total_scored if score else None
    
    return render_template('user/quizzes.html', 
                          chapter=chapter, 
                          quizzes=quizzes,
                          title=f'Quizzes - {chapter.name}')

@user_bp.route('/quizzes/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Check if already attempted
    previous_attempt = Score.query.filter_by(quiz_id=quiz_id, user_id=current_user.id).first()
    
    return render_template('user/take_quiz.html', 
                          quiz=quiz, 
                          questions=questions,
                          previous_attempt=previous_attempt,
                          title=f'Quiz - {quiz.chapter.name}')

@user_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Calculate score
    total_score = 0
    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        if user_answer and int(user_answer) == question.correct_answer:
            total_score += 1
    
    # Save score
    score = Score(
        quiz_id=quiz_id,
        user_id=current_user.id,
        time_stamp_of_attempt=datetime.utcnow(),
        total_scored=total_score
    )
    db.session.add(score)
    db.session.commit()
    
    flash(f'Quiz submitted! Your score: {total_score}/{len(questions)}', 'success')
    return redirect(url_for('user.results', score_id=score.id))

@user_bp.route('/results/<int:score_id>')
@login_required
def results(score_id):
    score = Score.query.get_or_404(score_id)
    
    # Ensure the score belongs to the current user
    if score.user_id != current_user.id:
        flash('You do not have permission to view these results.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    quiz = Quiz.query.get(score.quiz_id)
    questions = Question.query.filter_by(quiz_id=score.quiz_id).all()
    
    return render_template('user/results.html', 
                          score=score, 
                          quiz=quiz,
                          questions=questions,
                          title='Quiz Results') 