/**
 * B.Tech Viva Demo & LinkedIn Simulation Script
 * Provides a bulletproof, automated sequence to demonstrate multimodal confusion fusion
 */

window.isDemoMode = false;

// Custom Toast helper
function showDemoToast(message, icon = '🔧') {
    // Remove existing demo toasts
    const existingToasts = document.querySelectorAll('.demo-toast');
    existingToasts.forEach(t => t.remove());

    const toast = document.createElement('div');
    toast.className = 'demo-toast';
    toast.innerHTML = `<span>${icon}</span> ${message}`;
    document.body.appendChild(toast);

    // Fade out after 4 seconds
    setTimeout(() => {
        toast.style.transition = 'opacity 0.5s, transform 0.5s';
        toast.style.opacity = '0';
        toast.style.transform = 'translate(-50%, -30px)';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}

// Simulated smooth animation counter helper
function animateValue(setter, start, end, duration, onComplete) {
    const range = end - start;
    let current = start;
    const increment = end > start ? 0.02 : -0.02;
    const stepTime = Math.abs(Math.floor(duration / (range / 0.02)));
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            clearInterval(timer);
            setter(end);
            if (onComplete) onComplete();
        } else {
            setter(current);
        }
    }, stepTime);
}

/**
 * Run the automated confusion struggle timeline
 */
function startDemoSimulation() {
    if (window.isDemoMode) return;
    window.isDemoMode = true;
    
    console.log('🎬 B.Tech Viva Simulation Started...');
    showDemoToast('Viva Simulation Mode Active: Simulating Student Struggle...', '🚀');

    // References to UI elements
    const debugEmotion = document.getElementById('debugEmotion');
    const debugBehavior = document.getElementById('debugBehavior');
    const debugVideo = document.getElementById('debugVideo');

    // Freeze regular tracking checks
    if (window.behaviorCheckInterval) clearInterval(window.behaviorCheckInterval);
    if (window.videoCheckInterval) clearInterval(window.videoCheckInterval);

    let currentEmotion = 0.05;
    let currentBehavior = 0.10;
    let currentVideo = 0.00;

    // Helper to calculate score and update UI
    function updateDemoStatus() {
        // Weights: 40% Emotion, 30% Behavior, 30% Video
        const score = (currentEmotion * 0.4) + (currentBehavior * 0.3) + (currentVideo * 0.3);
        
        // Update debug labels
        if (debugEmotion) debugEmotion.textContent = currentEmotion.toFixed(2);
        if (debugBehavior) debugBehavior.textContent = currentBehavior.toFixed(2);
        if (debugVideo) debugVideo.textContent = currentVideo.toFixed(2);
        
        // Update main confusion bar
        if (typeof updateConfusionScore === 'function') {
            updateConfusionScore(score);
        }
        
        // Dynamic score text color styling based on urgency
        const scoreText = document.getElementById('scoreText');
        const scoreFill = document.getElementById('scoreFill');
        if (scoreText && scoreFill) {
            if (score >= 0.6) {
                scoreText.style.color = 'var(--danger-color)';
                scoreFill.style.color = 'var(--danger-color)';
            } else if (score >= 0.3) {
                scoreText.style.color = 'var(--warning-color)';
                scoreFill.style.color = 'var(--warning-color)';
            } else {
                scoreText.style.color = 'var(--success-color)';
                scoreFill.style.color = 'var(--success-color)';
            }
        }
    }

    // Step 1: Emotion score surges (0s - 3s)
    setTimeout(() => {
        showDemoToast('Facial Heuristics: Detecting expressions of frustration...', '📷');
        animateValue(
            (val) => { currentEmotion = val; updateDemoStatus(); },
            0.05, 0.78, 2500
        );
    }, 1000);

    // Step 2: Behavior score surges (3.5s - 6.5s)
    setTimeout(() => {
        showDemoToast('Interaction Telemetry: Low cursor velocity & key deletions...', '🖱️');
        animateValue(
            (val) => { currentBehavior = val; updateDemoStatus(); },
            0.10, 0.82, 2500
        );
    }, 4500);

    // Step 3: Video interaction pauses and rewinds (7s - 10s)
    setTimeout(() => {
        showDemoToast('Video player telemetric: 3 pauses and 2 rewinds detected...', '⏸️');
        animateValue(
            (val) => { currentVideo = val; updateDemoStatus(); },
            0.00, 0.85, 2500
        );
    }, 8000);

    // Step 4: Fusion Threshold Exceeded -> Trigger Glassmorphic Intervention Modal
    setTimeout(() => {
        showDemoToast('Multimodal Fusion Engine: Triggering Context-Aware Intervention!', '💡');
        
        const mockRecommendation = {
            show_intervention: true,
            intervention_type: 'concept_recap',
            content: {
                icon: '💡',
                title: 'Need a Concept Recap?',
                message: 'Based on your facial cues, cursor hesitation, and video pauses, you might be finding this concept challenging. Would you like a brief interactive summary?'
            }
        };
        
        const mockConfusionData = {
            smoothed_score: 0.813,
            explanation: {
                primary_explanation: 'Frequent video rewinding and cursor hesitation detected',
                primary_score: 0.85
            }
        };

        if (typeof showIntervention === 'function') {
            showIntervention(mockRecommendation, mockConfusionData);
        }
    }, 11500);

    // Step 5: User accepts help, hides modal, and transitions to Knowledge Check
    setTimeout(() => {
        showDemoToast('Student accepts recap. Transitioning to Knowledge Check Quiz...', '✅');
        
        // Trigger simulated check acceptance feedback
        if (typeof handleFeedback === 'function') {
            handleFeedback(true);
        }
        
        // Freeze final score and trigger transition to quiz
        const finalOverallScore = (currentEmotion * 0.4) + (currentBehavior * 0.3) + (currentVideo * 0.3);
        window.finalVideoConfusion = finalOverallScore;
        
        // Hide dashboard and show Quiz
        const mainContent = document.querySelector('.main-content');
        const quizSection = document.getElementById('quiz-section');
        if (mainContent && quizSection) {
            mainContent.style.opacity = '0';
            mainContent.style.transition = 'opacity 0.5s';
            setTimeout(() => {
                mainContent.style.display = 'none';
                quizSection.style.display = 'block';
                quizSection.style.opacity = '1';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }, 500);
        }
    }, 15000);

    // Step 6: Autofill Quiz inputs and calculate final Synchronized Confusion Index
    setTimeout(() => {
        showDemoToast('Final Sync Phase: Automatically logging quiz results...', '📊');
        
        const totalInput = document.getElementById('totalQuestionsInput');
        const correctInput = document.getElementById('correctAnswersInput');
        
        if (totalInput && correctInput) {
            totalInput.value = 5;
            correctInput.value = 2; // Student correct 2/5 (struggled)
            
            // Focus style simulation
            totalInput.style.borderColor = 'var(--primary-color)';
            correctInput.style.borderColor = 'var(--primary-color)';
        }
    }, 17500);

    // Step 7: Click sync calculation button to showcase results widget
    setTimeout(() => {
        showDemoToast('Sync complete! Generating final user confusion graph.', '📈');
        const syncButton = document.getElementById('syncScoreBtn');
        if (syncButton) {
            syncButton.click(); // Trigger quiz scoring calculations
            
            // Toast celebration
            setTimeout(() => {
                showDemoToast('Demo Completed Successfully! UI & backend fully synced. 🎉', '🏆');
                window.isDemoMode = false;
            }, 2500);
        }
    }, 19500);
}

// Bind simulation hotkey D
document.addEventListener('keydown', (event) => {
    if ((event.key === 'd' || event.key === 'D') && !window.isDemoMode) {
        // Only run if not typing in form inputs
        if (document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            startDemoSimulation();
        }
    }
});

console.log('⚡ Demo Mode script successfully linked! Press [D] to trigger struggle sequence.');
