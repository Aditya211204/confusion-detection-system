"""
Data Logging Utilities
Handles session data logging to CSV files
Tracks all confusion signals and interventions
"""

import os
import csv
from datetime import datetime
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LOGGING_CONFIG


class DataLogger:
    """
    Logs session data to CSV files for analysis
    Tracks: emotion scores, behavioral scores, confusion scores, interventions
    """
    
    def __init__(self):
        """Initialize logger with CSV file setup"""
        self.log_dir = LOGGING_CONFIG['log_directory']
        self.session_log_file = os.path.join(self.log_dir, LOGGING_CONFIG['session_log_file'])
        self.feedback_log_file = os.path.join(self.log_dir, LOGGING_CONFIG['feedback_log_file'])
        
        # Create log directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Initialize CSV files with headers
        self._initialize_session_log()
        self._initialize_feedback_log()
        
        print(f"[DataLogger] Initialized - Logs: {self.log_dir}")
    
    def _initialize_session_log(self):
        """Create session log CSV with headers if it doesn't exist"""
        if not os.path.exists(self.session_log_file):
            headers = [
                'timestamp',
                'emotion_score',
                'behavior_score',
                'video_score',
                'raw_confusion_score',
                'smoothed_confusion_score',
                'intervention_triggered',
                'primary_factor',
                'session_id'
            ]
            
            with open(self.session_log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def _initialize_feedback_log(self):
        """Create feedback log CSV with headers if it doesn't exist"""
        if not os.path.exists(self.feedback_log_file):
            headers = [
                'timestamp',
                'intervention_type',
                'was_helpful',
                'confusion_score',
                'session_id'
            ]
            
            with open(self.feedback_log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def log_session_data(self, emotion_score, behavior_score, video_score,
                        raw_score, smoothed_score, intervention_triggered,
                        primary_factor, session_id='default'):
        """
        Log session data to CSV
        
        Args:
            emotion_score: Emotion confusion score
            behavior_score: Behavioral confusion score
            video_score: Video interaction confusion score
            raw_score: Raw fused confusion score
            smoothed_score: Smoothed confusion score
            intervention_triggered: Whether intervention was triggered
            primary_factor: Primary confusion source
            session_id: Session identifier
        """
        try:
            row = [
                datetime.now().isoformat(),
                round(emotion_score, 3),
                round(behavior_score, 3),
                round(video_score, 3),
                round(raw_score, 3),
                round(smoothed_score, 3),
                intervention_triggered,
                primary_factor,
                session_id
            ]
            
            with open(self.session_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
                
        except Exception as e:
            print(f"[DataLogger] Error logging session data: {e}")
    
    def log_feedback(self, intervention_type, was_helpful, confusion_score, session_id='default'):
        """
        Log user feedback to CSV
        
        Args:
            intervention_type: Type of intervention shown
            was_helpful: Whether user found it helpful
            confusion_score: Confusion score when intervention was shown
            session_id: Session identifier
        """
        try:
            row = [
                datetime.now().isoformat(),
                intervention_type,
                was_helpful,
                round(confusion_score, 3),
                session_id
            ]
            
            with open(self.feedback_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
                
        except Exception as e:
            print(f"[DataLogger] Error logging feedback: {e}")
    
    def get_session_summary(self, session_id='default'):
        """
        Get summary statistics for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            dict: Session summary statistics
        """
        try:
            total_records = 0
            interventions_triggered = 0
            avg_confusion = 0.0
            
            with open(self.session_log_file, 'r') as f:
                reader = csv.DictReader(f)
                scores = []
                
                for row in reader:
                    if row['session_id'] == session_id:
                        total_records += 1
                        scores.append(float(row['smoothed_confusion_score']))
                        if row['intervention_triggered'] == 'True':
                            interventions_triggered += 1
                
                if scores:
                    avg_confusion = sum(scores) / len(scores)
            
            return {
                'session_id': session_id,
                'total_records': total_records,
                'interventions_triggered': interventions_triggered,
                'average_confusion_score': round(avg_confusion, 3)
            }
            
        except Exception as e:
            print(f"[DataLogger] Error getting session summary: {e}")
            return {}


# Singleton instance
data_logger = DataLogger()


def log_session_data(emotion_score, behavior_score, video_score,
                    raw_score, smoothed_score, intervention_triggered,
                    primary_factor, session_id='default'):
    """Public API for logging session data"""
    data_logger.log_session_data(
        emotion_score, behavior_score, video_score,
        raw_score, smoothed_score, intervention_triggered,
        primary_factor, session_id
    )


def log_feedback(intervention_type, was_helpful, confusion_score, session_id='default'):
    """Public API for logging feedback"""
    data_logger.log_feedback(intervention_type, was_helpful, confusion_score, session_id)


def get_session_summary(session_id='default'):
    """Public API for getting session summary"""
    return data_logger.get_session_summary(session_id)
