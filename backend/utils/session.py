"""
Session Management Utilities
Handles session creation, tracking, and cleanup
"""

import uuid
from datetime import datetime


class SessionManager:
    """
    Manages user learning sessions
    Tracks session state and metadata
    """
    
    def __init__(self):
        """Initialize session manager"""
        self.active_sessions = {}
        print("[SessionManager] Initialized")
    
    def create_session(self, user_id='anonymous', session_id=None):
        """
        Create a new learning session
        
        Args:
            user_id: User identifier (default: anonymous)
            session_id: Optional existing session ID
            
        Returns:
            str: Session ID
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        self.active_sessions[session_id] = {
            'user_id': user_id,
            'start_time': datetime.now(),
            'last_activity': datetime.now(),
            'intervention_count': 0,
            'confusion_events': 0
        }
        
        print(f"[SessionManager] Created session: {session_id}")
        return session_id
    
    def update_session(self, session_id, confusion_detected=False, intervention_triggered=False):
        """
        Update session activity
        
        Args:
            session_id: Session identifier
            confusion_detected: Whether confusion was detected
            intervention_triggered: Whether intervention was triggered
        """
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session['last_activity'] = datetime.now()
            
            if confusion_detected:
                session['confusion_events'] += 1
            
            if intervention_triggered:
                session['intervention_count'] += 1
    
    def get_session(self, session_id):
        """
        Get session data
        
        Args:
            session_id: Session identifier
            
        Returns:
            dict: Session data or None
        """
        return self.active_sessions.get(session_id)
    
    def end_session(self, session_id):
        """
        End a session and return summary
        
        Args:
            session_id: Session identifier
            
        Returns:
            dict: Session summary
        """
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            duration = (datetime.now() - session['start_time']).total_seconds()
            
            summary = {
                'session_id': session_id,
                'duration_seconds': round(duration, 2),
                'intervention_count': session['intervention_count'],
                'confusion_events': session['confusion_events']
            }
            
            # Remove from active sessions
            del self.active_sessions[session_id]
            
            print(f"[SessionManager] Ended session: {session_id}")
            return summary
        
        return None


# Singleton instance
session_manager = SessionManager()


def create_session(user_id='anonymous', session_id=None):
    """Public API for creating session"""
    return session_manager.create_session(user_id, session_id)


def update_session(session_id, confusion_detected=False, intervention_triggered=False):
    """Public API for updating session"""
    session_manager.update_session(session_id, confusion_detected, intervention_triggered)


def get_session(session_id):
    """Public API for getting session"""
    return session_manager.get_session(session_id)


def end_session(session_id):
    """Public API for ending session"""
    return session_manager.end_session(session_id)
