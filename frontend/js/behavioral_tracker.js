/**
 * Behavioral Tracker - Monitors mouse, keyboard, and video interactions
 * Detects confusion patterns in user behavior
 */

// Tracking state
let mouseTracking = {
    lastMovement: Date.now(),
    movementCount: 0,
    hesitationCount: 0,
    lastPosition: { x: 0, y: 0 }
};

let keyboardTracking = {
    lastKeystroke: Date.now(),
    typingSpeed: 0,
    deletionCount: 0,
    keystrokeCount: 0,
    startTime: Date.now()
};

let videoTracking = {
    pauseCount: 0,
    rewindCount: 0,
    replayCount: 0,
    lastPosition: 0,
    trackingStartTime: Date.now()
};

let behaviorCheckInterval = null;
let lastBehaviorScore = 0.0;
let player = null; // YouTube Player instance
let videoCheckInterval = null; // Interval for checking video time

/**
 * YouTube API Ready Callback
 */
window.onYouTubeIframeAPIReady = function () {
    console.log('📺 YouTube API Ready');
    
    // Attempt to extract video ID from the existing iframe src
    const iframe = document.getElementById('learningVideo');
    let videoId = 'M7lc1UVf-VE'; // Fallback default
    
    if (iframe && iframe.src) {
        const url = iframe.src;
        // Handle various YouTube URL formats:
        const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        const match = url.match(regExp);
        
        if (match && match[2].length === 11) {
            videoId = match[2];
            console.log(`🎥 Using video ID extracted from source: ${videoId}`);

            // CRITICAL FIX: If the URL is NOT in embed format, it will fail to load (Refused to connect)
            // We automatically update it to the correct embed format.
            if (!url.includes('/embed/')) {
                const newEmbedUrl = `https://www.youtube.com/embed/${videoId}?enablejsapi=1`;
                console.log(`🔄 Auto-converting to embed format: ${newEmbedUrl}`);
                iframe.src = newEmbedUrl;
            } else if (!url.includes('enablejsapi=1')) {
                iframe.src = url + (url.includes('?') ? '&' : '?') + 'enablejsapi=1';
            }
        }
    }

    player = new YT.Player('learningVideo', {
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
};

// Fallback: If YT API is already loaded before this script runs, trigger initialization manually
if (window.YT && window.YT.Player) {
    console.log('📺 YT API already loaded, manually triggering ready event.');
    window.onYouTubeIframeAPIReady();
}

function onPlayerReady(event) {
    console.log('📺 YouTube Player Initialized');
    // Start tracking video position
    videoCheckInterval = setInterval(checkVideoSeek, 1000);
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        handleVideoPlay();
    } else if (event.data == YT.PlayerState.PAUSED) {
        handleVideoPause();
    } else if (event.data == YT.PlayerState.ENDED) {
        handleVideoEnd();
    }
}

/**
 * Handle video completion
 */
function handleVideoEnd() {
    console.log('🎬 Video completed! Transitioning to quiz...');

    // 1. STOP ALL TRACKING
    if (videoCheckInterval) clearInterval(videoCheckInterval);
    if (behaviorCheckInterval) clearInterval(behaviorCheckInterval);
    
    // Stop webcam frames if function exists
    if (typeof stopWebcam === 'function') stopWebcam();

    // 2. CAPTURE FINAL VIDEO PHASE SCORE
    // Calculate final video stage score (Average of emotion, behavior, video)
    const emotionScore = (typeof getLastEmotionScore === 'function') ? getLastEmotionScore() : 0;
    const behaviorScore = lastBehaviorScore;
    const videoScore = calculateVideoScore();
    
    // Using the 40/30/30 weights as defined in logic
    const videoStageResult = (emotionScore * 0.4 + behaviorScore * 0.3 + videoScore * 0.3);
    
    // Store in global window variable for the sync button to use
    window.finalVideoConfusion = videoStageResult;
    console.log(`🔒 Tracking frozen. Final video-phase confusion: ${(videoStageResult * 100).toFixed(1)}%`);

    // 3. UI TRANSITION
    const mainContent = document.querySelector('.main-content');
    const quizSection = document.getElementById('quiz-section');

    if (mainContent && quizSection) {
        mainContent.style.display = 'none';
        quizSection.style.display = 'block';

        // Scroll to top of quiz
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}


/**
 * Initialize behavioral tracking
 */
function initializeBehavioralTracking() {
    console.log('🎯 Initializing behavioral tracking...');

    // Mouse tracking
    document.addEventListener('mousemove', handleMouseMove);

    // Keyboard tracking
    document.addEventListener('keydown', handleKeyPress);

    // Video tracking is handled by YouTube API callbacks

    // Periodic behavior analysis (every 5 seconds)
    behaviorCheckInterval = setInterval(async () => {
        await analyzeBehavior();
    }, 5000);

    console.log('✅ Behavioral tracking initialized');
}

/**
 * Handle mouse movement
 */
function handleMouseMove(event) {
    const now = Date.now();
    const timeSinceLastMove = (now - mouseTracking.lastMovement) / 1000;

    // Check for hesitation (back-and-forth movement)
    const deltaX = Math.abs(event.clientX - mouseTracking.lastPosition.x);
    const deltaY = Math.abs(event.clientY - mouseTracking.lastPosition.y);

    if (deltaX < 50 && deltaY < 50 && timeSinceLastMove < 0.5) {
        mouseTracking.hesitationCount++;
    }

    mouseTracking.lastMovement = now;
    mouseTracking.movementCount++;
    mouseTracking.lastPosition = { x: event.clientX, y: event.clientY };
}

/**
 * Handle keyboard press
 */
function handleKeyPress(event) {
    const now = Date.now();

    // Track deletions (backspace/delete)
    if (event.key === 'Backspace' || event.key === 'Delete') {
        keyboardTracking.deletionCount++;
    }

    keyboardTracking.lastKeystroke = now;
    keyboardTracking.keystrokeCount++;

    // Calculate typing speed (characters per minute)
    const timeElapsed = (now - keyboardTracking.startTime) / 1000 / 60; // minutes
    keyboardTracking.typingSpeed = keyboardTracking.keystrokeCount / timeElapsed;
}

/**
 * Handle video pause
 */
function handleVideoPause() {
    videoTracking.pauseCount++;
    console.log(`⏸️ Video paused (total: ${videoTracking.pauseCount})`);
}

/**
 * Handle video seek (simulated for YouTube)
 */
function checkVideoSeek() {
    if (!player || typeof player.getCurrentTime !== 'function') return;

    // Only check if we are in a state where time should be consistent
    const state = player.getPlayerState();
    if (state !== YT.PlayerState.PLAYING && state !== YT.PlayerState.PAUSED) return;

    const currentPosition = player.getCurrentTime();
    const timeDiff = currentPosition - videoTracking.lastPosition;

    // Detect rewind (current time is significantly less than last position)
    // We expect time to advance by ~1s per second when playing.
    // If it goes back, it's a rewind.

    // Threshold: -0.5s to account for minor drifts/jitter
    if (timeDiff < -0.5) {
        videoTracking.rewindCount++;

        // Check if replaying same segment (rewind within 30 seconds)
        if (Math.abs(timeDiff) < 30) {
            videoTracking.replayCount++;
        }

        console.log(`⏪ Video rewound (total: ${videoTracking.rewindCount})`);
    } else if (timeDiff > 2.0 && state === YT.PlayerState.PLAYING) {
        // Forward seek (skipped content)
        // We don't track skip count specifically in the object, but could be useful.
    }

    // Update last position
    videoTracking.lastPosition = currentPosition;
}

/**
 * Handle video play
 */
function handleVideoPlay() {
    if (player && typeof player.getCurrentTime === 'function') {
        videoTracking.lastPosition = player.getCurrentTime();
    }
}

/**
 * Analyze behavioral patterns and send to backend
 */
async function analyzeBehavior() {
    const now = Date.now();

    // Calculate inactivity durations
    const mouseInactivity = (now - mouseTracking.lastMovement) / 1000;
    const keyboardPause = (now - keyboardTracking.lastKeystroke) / 1000;

    // Prepare data for backend
    const mouseData = {
        inactivity_duration: mouseInactivity,
        movement_count: mouseTracking.movementCount,
        hesitation_count: mouseTracking.hesitationCount
    };

    const keyboardData = {
        pause_duration: keyboardPause,
        typing_speed: keyboardTracking.typingSpeed,
        deletion_count: keyboardTracking.deletionCount
    };

    const videoData = {
        pause_count: videoTracking.pauseCount,
        rewind_count: videoTracking.rewindCount,
        replay_count: videoTracking.replayCount
    };

    // Send to backend
    // Check if sendBehavioralData is defined
    if (typeof sendBehavioralData === 'function') {
        const result = await sendBehavioralData(mouseData, keyboardData, videoData);

        if (result.success) {
            lastBehaviorScore = result.overall_behavior_score;

            // Update debug panel
            updateDebugInfo('behavior', lastBehaviorScore);

            console.log(`🖱️ Behavior analyzed - Score: ${(lastBehaviorScore * 100).toFixed(1)}%`);

            // Check for intervention
            await checkForIntervention();
        }
    } else {
        console.warn('sendBehavioralData is not defined');
    }

    // Reset counters for next window
    mouseTracking.movementCount = 0;
    mouseTracking.hesitationCount = 0;
    keyboardTracking.deletionCount = 0;
}

async function checkForIntervention() {
    const emotionScore = (typeof getLastEmotionScore === 'function') ? getLastEmotionScore() : 0;
    const behaviorScore = lastBehaviorScore;
    const videoScore = calculateVideoScore();

    // Update debug panel
    updateDebugInfo('video', videoScore);

    // Update confusion score display
    const overallScore = (emotionScore * 0.4 + behaviorScore * 0.3 + videoScore * 0.3);
    updateConfusionScore(overallScore);

    // Check intervention
    if (typeof checkIntervention === 'function') {
        const result = await checkIntervention(emotionScore, behaviorScore, videoScore);

        if (result.success) {
            // Update session stats from backend
            if (result.session_stats) {
                updateSessionStats(result.session_stats);
            }

            if (result.intervention_needed && result.recommendation) {
                showIntervention(result.recommendation, result.confusion_data);
            }
        }
    }
}

/**
 * Calculate video interaction confusion score
 */
function calculateVideoScore() {
    const now = Date.now();
    const timeWindow = (now - videoTracking.trackingStartTime) / 1000 / 60; // minutes

    if (timeWindow <= 0) return 0;

    // Normalize counts to 5-minute window
    const normalizedPauses = (videoTracking.pauseCount / timeWindow) * 5;
    const normalizedRewinds = (videoTracking.rewindCount / timeWindow) * 5;
    const normalizedReplays = (videoTracking.replayCount / timeWindow) * 5;

    // Calculate score (same logic as backend)
    const pauseScore = Math.min(normalizedPauses / 5, 1.0);
    const rewindScore = Math.min(normalizedRewinds / 3, 1.0);
    const replayScore = Math.min(normalizedReplays / 2, 1.0);

    return pauseScore * 0.4 + rewindScore * 0.3 + replayScore * 0.3;
}

/**
 * Update confusion score display
 */
function updateConfusionScore(score) {
    const scoreFill = document.getElementById('scoreFill');
    const scoreText = document.getElementById('scoreText');

    if (scoreFill && scoreText) {
        const percentage = Math.round(score * 100);
        scoreFill.style.width = `${percentage}%`;
        scoreText.textContent = `${percentage}%`;
    }
}

/**
 * Update debug panel
 */
function updateDebugInfo(type, score) {
    const debugElements = {
        'emotion': 'debugEmotion',
        'behavior': 'debugBehavior',
        'video': 'debugVideo'
    };

    const elementId = debugElements[type];
    if (elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = score.toFixed(2);
        }
    }
}

/**
 * Update session stats from backend
 */
function updateSessionStats(sessionStats) {
    const interventionElement = document.getElementById('debugInterventions');
    if (interventionElement && sessionStats.intervention_count !== undefined) {
        interventionElement.textContent = sessionStats.intervention_count;
    }
}

/**
 * Get last behavior score
 */
function getLastBehaviorScore() {
    return lastBehaviorScore;
}
