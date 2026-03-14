/**
 * API Client - Centralized backend communication
 * Handles all HTTP requests to Flask backend
 */

const API_BASE_URL = 'http://127.0.0.1:5000/api';

/**
 * Get or create session ID
 * @returns {string} Session ID (UUID)
 */
function getSessionId() {
    let sessionId = localStorage.getItem('session_id');

    if (!sessionId) {
        // Generate UUID v4
        sessionId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });

        localStorage.setItem('session_id', sessionId);
        console.log('🆔 Created new session ID:', sessionId);
    }

    return sessionId;
}

/**
 * Send emotion data to backend
 * @param {string} base64Image - Base64 encoded webcam frame
 * @returns {Promise<Object>} Emotion analysis result
 */
async function sendEmotionData(base64Image) {
    try {
        const response = await fetch(`${API_BASE_URL}/emotion/detect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: base64Image })
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error sending emotion data:', error);
        return { success: false, error: error.message, confusion_score: 0.0 };
    }
}

/**
 * Send behavioral data to backend
 * @param {Object} mouseData - Mouse tracking data
 * @param {Object} keyboardData - Keyboard tracking data
 * @param {Object} videoData - Video interaction data
 * @returns {Promise<Object>} Behavioral analysis result
 */
async function sendBehavioralData(mouseData, keyboardData, videoData) {
    try {
        const response = await fetch(`${API_BASE_URL}/behavior/track`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mouse_data: mouseData,
                keyboard_data: keyboardData,
                video_data: videoData
            })
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error sending behavioral data:', error);
        return { success: false, error: error.message, overall_behavior_score: 0.0 };
    }
}

/**
 * Check if intervention is needed
 * @param {number} emotionScore - Emotion confusion score
 * @param {number} behaviorScore - Behavioral confusion score
 * @param {number} videoScore - Video interaction confusion score
 * @returns {Promise<Object>} Intervention check result
 */
async function checkIntervention(emotionScore, behaviorScore, videoScore) {
    try {
        const response = await fetch(`${API_BASE_URL}/intervention/check`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': getSessionId()
            },
            body: JSON.stringify({
                emotion_score: emotionScore,
                behavior_score: behaviorScore,
                video_score: videoScore
            })
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error checking intervention:', error);
        return { success: false, error: error.message, intervention_needed: false };
    }
}

/**
 * Send user feedback on intervention
 * @param {string} interventionType - Type of intervention shown
 * @param {boolean} wasHelpful - Whether user found it helpful
 * @returns {Promise<Object>} Feedback submission result
 */
async function sendFeedback(interventionType, wasHelpful) {
    try {
        const response = await fetch(`${API_BASE_URL}/intervention/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                intervention_type: interventionType,
                was_helpful: wasHelpful
            })
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error sending feedback:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get feedback statistics
 * @returns {Promise<Object>} Feedback statistics
 */
async function getFeedbackStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/intervention/stats`, {
            method: 'GET'
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error getting feedback stats:', error);
        return { success: false, error: error.message };
    }
}
