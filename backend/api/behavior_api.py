"""
Flask API Endpoints for Behavioral Analysis
Handles mouse, keyboard, and video interaction tracking
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.behavior_model import analyze_behavior

# Create Blueprint
behavior_bp = Blueprint('behavior', __name__, url_prefix='/api/behavior')


@behavior_bp.route('/track', methods=['POST'])
def track_behavior():
    """
    Analyze behavioral patterns for confusion signals
    
    Request Body:
        {
            "mouse_data": {
                "inactivity_duration": 25,
                "movement_count": 3,
                "hesitation_count": 2
            },
            "keyboard_data": {
                "pause_duration": 18,
                "typing_speed": 15,
                "deletion_count": 7
            },
            "video_data": {
                "pause_count": 4,
                "rewind_count": 2,
                "replay_count": 1
            }
        }
    
    Response:
        {
            "success": true,
            "mouse_score": 0.45,
            "keyboard_score": 0.62,
            "video_score": 0.58,
            "overall_behavior_score": 0.55
        }
    """
    try:
        # Get behavioral data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Extract individual data components
        mouse_data = data.get('mouse_data', {})
        keyboard_data = data.get('keyboard_data', {})
        video_data = data.get('video_data', {})
        
        # Analyze behavior
        result = analyze_behavior(mouse_data, keyboard_data, video_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@behavior_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for behavioral analysis service"""
    return jsonify({
        'success': True,
        'service': 'behavioral_analysis',
        'status': 'running'
    }), 200
