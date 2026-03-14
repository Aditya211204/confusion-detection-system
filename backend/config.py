"""
Configuration file for AI-Based Silent Confusion Detection System
Contains all thresholds, weights, and system parameters
"""

# ==================== EMOTION DETECTION SETTINGS ====================
EMOTION_CONFIG = {
    'frame_capture_interval': 3,  # Capture webcam frame every 3 seconds
    'confidence_threshold': 0.5,   # Minimum confidence for emotion detection
    'target_emotions': ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'],
    'confusion_emotions': {
        'angry': 0.3,      # Weight for anger indicating frustration
        'disgust': 0.2,    # Weight for disgust
        'fear': 0.4,       # Weight for fear/anxiety
        'sad': 0.5,        # Weight for sadness/confusion
        'surprise': 0.1,   # Weight for surprise
        'neutral': 0.0,    # Neutral has no confusion weight
        'happy': -0.2      # Happy reduces confusion score
    }
}

# ==================== BEHAVIORAL ANALYSIS SETTINGS ====================
BEHAVIOR_CONFIG = {
    # Mouse tracking thresholds
    'mouse_inactivity_threshold': 30,  # Seconds of no mouse movement
    'mouse_hesitation_threshold': 5,   # Number of back-and-forth movements
    
    # Keyboard tracking thresholds
    'typing_pause_threshold': 15,      # Seconds of no typing
    'typing_speed_threshold': 20,      # Characters per minute (low = confusion)
    
    # Video interaction thresholds
    'pause_frequency_threshold': 5,    # Number of pauses in 5 minutes
    'rewind_frequency_threshold': 3,   # Number of rewinds in 5 minutes
    'replay_segment_threshold': 2      # Replaying same segment multiple times
}

# ==================== CONFUSION FUSION WEIGHTS ====================
FUSION_CONFIG = {
    'emotion_weight': 0.4,      # 40% weight for emotion signals
    'behavior_weight': 0.3,     # 30% weight for behavioral signals
    'video_weight': 0.3,        # 30% weight for video interaction signals
    'temporal_window': 5,       # Moving average window (smoothing)
    'confusion_threshold': 0.6  # Trigger intervention when score > 0.6
}

# ==================== RECOMMENDATION ENGINE SETTINGS ====================
RECOMMENDATION_CONFIG = {
    'intervention_types': [
        'simpler_explanation',
        'real_life_example',
        'short_quiz',
        'concept_recap'
    ],
    'cooldown_period': 120,     # Seconds before showing another intervention
    'feedback_learning_rate': 0.1,  # How quickly to adapt based on feedback
    'min_confidence': 0.5       # Minimum confidence for recommendation
}

# ==================== DATA LOGGING SETTINGS ====================
LOGGING_CONFIG = {
    'log_directory': 'logs',
    'session_log_file': 'session_data.csv',
    'feedback_log_file': 'feedback_data.csv',
    'log_interval': 5,          # Log data every 5 seconds
    'enable_sqlite': False      # Set to True to use SQLite instead of CSV
}

# ==================== FLASK SERVER SETTINGS ====================
SERVER_CONFIG = {
    'host': '127.0.0.1',
    'port': 5000,
    'debug': True,
    'cors_origins': '*'         # Allow all origins for development
}
