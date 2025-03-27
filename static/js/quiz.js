// Quiz Timer and Management Script

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a quiz page
    const quizContainer = document.getElementById('quiz-container');
    if (!quizContainer) return;

    // Get quiz duration in minutes from data attribute
    const durationStr = quizContainer.dataset.duration || '30 minutes';
    let totalSeconds = 0;
    
    // Parse the duration string (e.g., "30 minutes", "1 hour")
    if (durationStr.includes('minute')) {
        totalSeconds = parseInt(durationStr) * 60;
    } else if (durationStr.includes('hour')) {
        totalSeconds = parseInt(durationStr) * 60 * 60;
    }
    
    // Fall back to 30 minutes if parsing fails
    if (!totalSeconds) {
        totalSeconds = 30 * 60;
    }
    
    let timer;
    const timerDisplay = document.getElementById('quiz-timer');
    
    // Format seconds as MM:SS
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    // Start the countdown
    function startTimer() {
        timerDisplay.innerText = formatTime(totalSeconds);
        
        timer = setInterval(function() {
            totalSeconds--;
            timerDisplay.innerText = formatTime(totalSeconds);
            
            // Change color to red when less than 5 minutes remain
            if (totalSeconds < 300) {
                timerDisplay.classList.add('text-danger');
            }
            
            // Auto-submit when time expires
            if (totalSeconds <= 0) {
                clearInterval(timer);
                document.getElementById('quiz-form').submit();
            }
        }, 1000);
    }
    
    // Start timer when page loads
    startTimer();
    
    // Validate that all questions are answered
    const quizForm = document.getElementById('quiz-form');
    if (quizForm) {
        quizForm.addEventListener('submit', function(e) {
            const questions = document.querySelectorAll('.question-card');
            let allAnswered = true;
            
            questions.forEach(question => {
                const questionId = question.dataset.questionId;
                const answered = document.querySelector(`input[name="question_${questionId}"]:checked`);
                
                if (!answered) {
                    allAnswered = false;
                    question.classList.add('border', 'border-danger');
                } else {
                    question.classList.remove('border', 'border-danger');
                }
            });
            
            if (!allAnswered) {
                e.preventDefault();
                alert('Please answer all questions before submitting.');
                window.scrollTo(0, 0);
            }
        });
    }
    
    // Confirmation for leaving the page
    window.addEventListener('beforeunload', function(e) {
        // Cancel the event
        e.preventDefault();
        // Chrome requires returnValue to be set
        e.returnValue = '';
    });
}); 