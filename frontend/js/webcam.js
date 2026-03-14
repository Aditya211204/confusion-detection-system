/**
 * Webcam Module - Handles webcam initialization and emotion detection
 * Captures frames periodically and sends to backend for analysis
 */

let webcamStream = null;
let emotionDetectionInterval = null;
let lastEmotionScore = 0.0;

/**
 * Initialize webcam and start emotion detection
 */
async function initializeWebcam() {
    try {
        console.log('📷 Initializing webcam...');

        // Request webcam access
        webcamStream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        });

        // Attach stream to video element
        const webcamFeed = document.getElementById('webcamFeed');
        webcamFeed.srcObject = webcamStream;

        console.log('✅ Webcam initialized');

        // Start periodic emotion detection (every 3 seconds)
        startEmotionDetection();

    } catch (error) {
        console.error('❌ Error initializing webcam:', error);
        alert('Webcam access denied. Emotion detection will not work.');
    }
}

/**
 * Start periodic emotion detection
 */
function startEmotionDetection() {
    // Capture and analyze frame every 3 seconds
    emotionDetectionInterval = setInterval(async () => {
        await captureAndAnalyzeFrame();
    }, 3000);

    console.log('🎯 Emotion detection started');
}

/**
 * Capture webcam frame and send for emotion analysis
 */
async function captureAndAnalyzeFrame() {
    try {
        const webcamFeed = document.getElementById('webcamFeed');

        // Create canvas to capture frame
        const canvas = document.createElement('canvas');
        canvas.width = webcamFeed.videoWidth;
        canvas.height = webcamFeed.videoHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(webcamFeed, 0, 0);

        // Convert to base64
        const base64Image = canvas.toDataURL('image/jpeg', 0.8);

        // Send to backend for emotion analysis
        const result = await sendEmotionData(base64Image);

        if (result.success) {
            lastEmotionScore = result.confusion_score;

            // Update debug panel
            updateDebugInfo('emotion', lastEmotionScore);

            console.log(`😊 Emotion detected - Confusion: ${(lastEmotionScore * 100).toFixed(1)}%`);
        } else {
            console.warn('⚠️ Emotion detection failed:', result.error);
        }

    } catch (error) {
        console.error('❌ Error capturing frame:', error);
    }
}

/**
 * Get last emotion score
 * @returns {number} Last emotion confusion score
 */
function getLastEmotionScore() {
    return lastEmotionScore;
}

/**
 * Stop webcam and emotion detection
 */
function stopWebcam() {
    if (emotionDetectionInterval) {
        clearInterval(emotionDetectionInterval);
    }

    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
    }

    console.log('🛑 Webcam stopped');
}
