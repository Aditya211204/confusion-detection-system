"""
Flask API Endpoints for Emotion Detection
Handles webcam frame processing and emotion analysis
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.emotion_model import analyze_emotion

# Create Blueprint
emotion_bp = Blueprint('emotion', __name__, url_prefix='/api/emotion')


@emotion_bp.route('/detect', methods=['POST'])
def detect_emotion():
    """
    Detect emotions from webcam frame
    
    Request Body:
        {
            "image": "base64_encoded_image_string"
        }
    
    Response:
        {
            "success": true,
            "emotions": {...},
            "confusion_score": 0.65,
            "face_detected": true
        }
    """
    try:
        # Get image from request
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'No image provided'
            }), 400
        
        base64_image = data['image']
        
        # Analyze emotion
        result = analyze_emotion(base64_image)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@emotion_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for emotion detection service"""
    return jsonify({
        'success': True,
        'service': 'emotion_detection',
        'status': 'running'
    }), 200
