"""
Flask API Endpoints for Intervention Management
Handles confusion checking and feedback recording
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.fusion_engine import fuse_confusion_scores
from models.recommendation import generate_recommendation, record_feedback, get_feedback_stats
from utils.session import create_session, update_session, get_session

# Create Blueprint
intervention_bp = Blueprint('intervention', __name__, url_prefix='/api/intervention')


@intervention_bp.route('/check', methods=['POST'])
def check_intervention():
    """
    Check if intervention is needed based on all confusion signals
    
    Request Headers:
        X-Session-ID: Session identifier (UUID)
    
    Request Body:
        {
            "emotion_score": 0.65,
            "behavior_score": 0.55,
            "video_score": 0.48
        }
    
    Response:
        {
            "success": true,
            "intervention_needed": true,
            "recommendation": {...},
            "confusion_data": {...},
            "session_stats": {
                "confusion_events": 5,
                "intervention_count": 3
            }
        }
    """
    try:
        # Get or create session
        session_id = request.headers.get('X-Session-ID')
        
        # Check if session exists in manager
        if session_id:
            existing_session = get_session(session_id)
            if not existing_session:
                # Session ID exists but session data missing (server restart?)
                # Re-create session with same ID
                create_session(session_id=session_id)
                print(f"[InterventionAPI] Re-created session: {session_id}")
        else:
            # Create completely new session
            session_id = create_session()
            print(f"[InterventionAPI] Created new session: {session_id}")
        
        # Get scores from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        emotion_score = data.get('emotion_score', 0.0)
        behavior_score = data.get('behavior_score', 0.0)
        video_score = data.get('video_score', 0.0)
        
        # Fuse confusion scores
        fusion_result = fuse_confusion_scores(emotion_score, behavior_score, video_score)
        
        # Determine if confusion was detected
        confusion_detected = fusion_result['intervention_needed']
        
        # If intervention needed, generate recommendation
        intervention_triggered = False
        recommendation = None
        
        if fusion_result['intervention_needed']:
            recommendation = generate_recommendation(fusion_result)
            intervention_triggered = recommendation.get('show_intervention', False)
        
        # Update session with separate tracking
        update_session(
            session_id,
            confusion_detected=confusion_detected,
            intervention_triggered=intervention_triggered
        )
        
        # Get session stats
        session_data = get_session(session_id)
        session_stats = {
            'confusion_events': session_data['confusion_events'] if session_data else 0,
            'intervention_count': session_data['intervention_count'] if session_data else 0
        }
        
        if intervention_triggered:
            return jsonify({
                'success': True,
                'intervention_needed': True,
                'recommendation': recommendation,
                'confusion_data': fusion_result,
                'session_stats': session_stats,
                'session_id': session_id
            }), 200
        else:
            return jsonify({
                'success': True,
                'intervention_needed': confusion_detected,
                'confusion_data': fusion_result,
                'session_stats': session_stats,
                'session_id': session_id
            }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@intervention_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """
    Record user feedback on intervention
    
    Request Body:
        {
            "intervention_type": "simpler_explanation",
            "was_helpful": true
        }
    
    Response:
        {
            "success": true,
            "message": "Feedback recorded"
        }
    """
    try:
        # Get feedback from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        intervention_type = data.get('intervention_type')
        was_helpful = data.get('was_helpful', False)
        
        if not intervention_type:
            return jsonify({
                'success': False,
                'error': 'intervention_type required'
            }), 400
        
        # Record feedback
        record_feedback(intervention_type, was_helpful)
        
        return jsonify({
            'success': True,
            'message': 'Feedback recorded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@intervention_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get feedback statistics for all intervention types
    
    Response:
        {
            "success": true,
            "stats": {...}
        }
    """
    try:
        stats = get_feedback_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@intervention_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for intervention service"""
    return jsonify({
        'success': True,
        'service': 'intervention_management',
        'status': 'running'
    }), 200
