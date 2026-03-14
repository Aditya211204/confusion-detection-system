/**
 * Intervention Module - Handles intervention popup display and feedback
 * Shows intelligent suggestions when confusion is detected
 */

let currentIntervention = null;

/**
 * Initialize intervention system
 */
function initializeInterventionSystem() {
    console.log('💡 Initializing intervention system...');

    // Set up event listeners for popup buttons
    const closeBtn = document.getElementById('closePopup');
    const helpfulBtn = document.getElementById('helpfulBtn');
    const dismissBtn = document.getElementById('dismissBtn');

    closeBtn.addEventListener('click', () => hideIntervention(false));
    helpfulBtn.addEventListener('click', () => handleFeedback(true));
    dismissBtn.addEventListener('click', () => handleFeedback(false));

    // Close popup when clicking outside
    const popup = document.getElementById('interventionPopup');
    popup.addEventListener('click', (event) => {
        if (event.target === popup) {
            hideIntervention(false);
        }
    });

    console.log('✅ Intervention system initialized');
}

/**
 * Show intervention popup
 * @param {Object} recommendation - Recommendation from backend
 * @param {Object} confusionData - Confusion analysis data
 */
function showIntervention(recommendation, confusionData) {
    // Check if intervention should be shown (cooldown check)
    if (!recommendation.show_intervention) {
        console.log('⏳ Intervention on cooldown');
        return;
    }

    console.log('💡 Showing intervention:', recommendation.intervention_type);

    // Store current intervention data
    currentIntervention = {
        type: recommendation.intervention_type,
        confusionScore: confusionData.smoothed_score
    };

    // Update popup content
    const popupIcon = document.getElementById('popupIcon');
    const popupTitle = document.getElementById('popupTitle');
    const popupMessage = document.getElementById('popupMessage');
    const explanationText = document.getElementById('explanationText');

    const content = recommendation.content;
    popupIcon.textContent = content.icon;
    popupTitle.textContent = content.title;
    popupMessage.textContent = content.message;

    // Update explanation
    const explanation = confusionData.explanation;
    explanationText.textContent = `Primary factor: ${explanation.primary_explanation} (${(explanation.primary_score * 100).toFixed(0)}% confidence)`;

    // Show popup with animation
    const popup = document.getElementById('interventionPopup');
    popup.classList.add('show');

    // Play subtle notification sound (optional)
    playNotificationSound();
}

/**
 * Hide intervention popup
 * @param {boolean} wasHelpful - Whether user found it helpful
 */
function hideIntervention(wasHelpful) {
    const popup = document.getElementById('interventionPopup');
    popup.classList.remove('show');

    console.log('❌ Intervention hidden');
}

/**
 * Handle user feedback
 * @param {boolean} wasHelpful - Whether user found intervention helpful
 */
async function handleFeedback(wasHelpful) {
    if (!currentIntervention) {
        return;
    }

    console.log(`📝 Feedback: ${wasHelpful ? 'Helpful' : 'Dismissed'}`);

    // Send feedback to backend
    await sendFeedback(currentIntervention.type, wasHelpful);

    // Hide popup
    hideIntervention(wasHelpful);

    // Show thank you message
    if (wasHelpful) {
        showThankYouMessage();
    }

    currentIntervention = null;
}

/**
 * Show thank you message
 */
function showThankYouMessage() {
    // Create temporary thank you notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        z-index: 2000;
        animation: slideInRight 0.3s ease;
    `;
    notification.textContent = '✅ Thank you for your feedback!';

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Play subtle notification sound
 */
function playNotificationSound() {
    // Create audio context for subtle beep
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.value = 800; // Hz
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    } catch (error) {
        // Silently fail if audio not supported
        console.log('Audio notification not available');
    }
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
