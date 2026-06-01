"""
Flask Application - AI-Based Silent Confusion Detection System
Main application file with route registration and server configuration
"""

from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import configuration
from config import SERVER_CONFIG

# Import API blueprints
from api.emotion_api import emotion_bp
from api.behavior_api import behavior_bp
from api.intervention_api import intervention_bp

# Import utilities
from utils.logger import data_logger
from utils.session import session_manager


def create_app():
    """
    Create and configure Flask application
    
    Returns:
        Flask: Configured Flask app
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    
    # Enable CORS for frontend communication
    CORS(app, resources={r"/api/*": {"origins": SERVER_CONFIG['cors_origins']}})
    
    # Register API blueprints
    app.register_blueprint(emotion_bp)
    app.register_blueprint(behavior_bp)
    app.register_blueprint(intervention_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        """Serve the frontend application"""
        return app.send_static_file('index.html')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        """Overall system health check"""
        return jsonify({
            'success': True,
            'status': 'healthy',
            'services': {
                'emotion_detection': 'running',
                'behavioral_analysis': 'running',
                'intervention_management': 'running',
                'data_logging': 'running'
            }
        })
    
    return app


if __name__ == '__main__':
    """Run Flask development server"""
    app = create_app()
    
    print("=" * 60)
    print("AI-Based Silent Confusion Detection System")
    print("=" * 60)
    print(f"Server running at: http://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}")
    print("API Endpoints:")
    print("  - POST /api/emotion/detect       - Detect emotions from webcam")
    print("  - POST /api/behavior/track       - Track behavioral patterns")
    print("  - POST /api/intervention/check   - Check if intervention needed")
    print("  - POST /api/intervention/feedback - Submit user feedback")
    print("  - GET  /api/intervention/stats   - Get feedback statistics")
    print("=" * 60)
    
    app.run(
        host=SERVER_CONFIG['host'],
        port=SERVER_CONFIG['port'],
        debug=SERVER_CONFIG['debug']
    )
