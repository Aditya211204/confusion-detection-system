"""
Behavioral Analysis Module
Analyzes mouse movements, keyboard typing patterns, and video interaction behavior
Calculates behavioral confusion score based on inactivity, hesitation, and interaction patterns
"""

import sys
import os
from datetime import datetime

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BEHAVIOR_CONFIG


class BehaviorAnalyzer:
    """
    Analyzes user behavioral patterns to detect confusion signals
    Tracks: mouse activity, keyboard activity, video interactions
    """
    
    def __init__(self):
        """Initialize behavior analyzer with configuration thresholds"""
        self.config = BEHAVIOR_CONFIG
        self.session_data = {
            'mouse_events': [],
            'keyboard_events': [],
            'video_events': []
        }
        print("[BehaviorAnalyzer] Initialized successfully")
    
    def analyze_mouse_behavior(self, mouse_data):
        """
        Analyze mouse movement patterns for confusion signals
        
        Confusion indicators:
        - Long periods of inactivity
        - Hesitation (back-and-forth movements)
        - Erratic movements
        
        Args:
            mouse_data: dict with keys:
                - inactivity_duration: seconds of no movement
                - movement_count: number of movements in window
                - hesitation_count: back-and-forth movements
                
        Returns:
            float: Mouse confusion score (0-1)
        """
        score = 0.0
        
        # Inactivity score (normalized by threshold)
        inactivity_duration = mouse_data.get('inactivity_duration', 0)
        inactivity_score = min(
            inactivity_duration / self.config['mouse_inactivity_threshold'],
            1.0
        )
        score += inactivity_score * 0.5  # 50% weight
        
        # Hesitation score
        hesitation_count = mouse_data.get('hesitation_count', 0)
        hesitation_score = min(
            hesitation_count / self.config['mouse_hesitation_threshold'],
            1.0
        )
        score += hesitation_score * 0.3  # 30% weight
        
        # Movement frequency score (too few movements = confusion)
        movement_count = mouse_data.get('movement_count', 0)
        if movement_count < 5:  # Very few movements in tracking window
            score += 0.2  # 20% weight
        
        return min(score, 1.0)
    
    def analyze_keyboard_behavior(self, keyboard_data):
        """
        Analyze keyboard typing patterns for confusion signals
        
        Confusion indicators:
        - Long typing pauses
        - Reduced typing speed
        - Frequent deletions (uncertainty)
        
        Args:
            keyboard_data: dict with keys:
                - pause_duration: seconds since last keystroke
                - typing_speed: characters per minute
                - deletion_count: number of backspace/delete presses
                
        Returns:
            float: Keyboard confusion score (0-1)
        """
        score = 0.0
        
        # Typing pause score
        pause_duration = keyboard_data.get('pause_duration', 0)
        pause_score = min(
            pause_duration / self.config['typing_pause_threshold'],
            1.0
        )
        score += pause_score * 0.4  # 40% weight
        
        # Typing speed score (lower speed = higher confusion)
        typing_speed = keyboard_data.get('typing_speed', 100)
        if typing_speed < self.config['typing_speed_threshold']:
            speed_score = 1.0 - (typing_speed / self.config['typing_speed_threshold'])
            score += speed_score * 0.4  # 40% weight
        
        # Deletion frequency (uncertainty indicator)
        deletion_count = keyboard_data.get('deletion_count', 0)
        if deletion_count > 5:  # Frequent deletions
            score += 0.2  # 20% weight
        
        return min(score, 1.0)
    
    def analyze_video_behavior(self, video_data):
        """
        Analyze video interaction patterns for confusion signals
        
        Confusion indicators:
        - Frequent pausing
        - Rewinding/replaying segments
        - Slow playback speed
        
        Args:
            video_data: dict with keys:
                - pause_count: number of pauses in time window
                - rewind_count: number of rewinds
                - replay_count: number of segment replays
                - playback_speed: current playback speed
                
        Returns:
            float: Video interaction confusion score (0-1)
        """
        score = 0.0
        
        # Pause frequency score
        pause_count = video_data.get('pause_count', 0)
        pause_score = min(
            pause_count / self.config['pause_frequency_threshold'],
            1.0
        )
        score += pause_score * 0.4  # 40% weight
        
        # Rewind frequency score
        rewind_count = video_data.get('rewind_count', 0)
        rewind_score = min(
            rewind_count / self.config['rewind_frequency_threshold'],
            1.0
        )
        score += rewind_score * 0.3  # 30% weight
        
        # Replay segment score (strong confusion indicator)
        replay_count = video_data.get('replay_count', 0)
        replay_score = min(
            replay_count / self.config['replay_segment_threshold'],
            1.0
        )
        score += replay_score * 0.3  # 30% weight
        
        return min(score, 1.0)
    
    def calculate_overall_behavior_score(self, mouse_data, keyboard_data, video_data):
        """
        Calculate combined behavioral confusion score
        
        Args:
            mouse_data: Mouse behavior data
            keyboard_data: Keyboard behavior data
            video_data: Video interaction data
            
        Returns:
            dict: Detailed behavioral analysis with overall score
        """
        # Calculate individual scores
        mouse_score = self.analyze_mouse_behavior(mouse_data)
        keyboard_score = self.analyze_keyboard_behavior(keyboard_data)
        video_score = self.analyze_video_behavior(video_data)
        
        # Weighted combination (equal weights for simplicity)
        overall_score = (mouse_score * 0.33 + 
                        keyboard_score * 0.33 + 
                        video_score * 0.34)
        
        return {
            'success': True,
            'mouse_score': round(mouse_score, 3),
            'keyboard_score': round(keyboard_score, 3),
            'video_score': round(video_score, 3),
            'overall_behavior_score': round(overall_score, 3),
            'timestamp': datetime.now().isoformat()
        }


# Singleton instance
behavior_analyzer = BehaviorAnalyzer()


def analyze_behavior(mouse_data, keyboard_data, video_data):
    """
    Public API function for behavioral analysis
    
    Args:
        mouse_data: Mouse tracking data
        keyboard_data: Keyboard tracking data
        video_data: Video interaction data
        
    Returns:
        dict: Behavioral analysis result with confusion score
    """
    return behavior_analyzer.calculate_overall_behavior_score(
        mouse_data, keyboard_data, video_data
    )
