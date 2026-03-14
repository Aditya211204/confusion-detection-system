"""
Confusion Fusion Engine
Combines emotion, behavioral, and video interaction scores into unified confusion score
Implements temporal smoothing and threshold-based decision making
Provides explainability for confusion detection
"""

import sys
import os
from collections import deque
from datetime import datetime

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FUSION_CONFIG


class ConfusionFusionEngine:
    """
    Fuses multiple confusion signals into a single score
    Applies temporal smoothing to avoid false positives
    Provides explainability for detected confusion
    """
    
    def __init__(self):
        """Initialize fusion engine with configuration and history tracking"""
        self.config = FUSION_CONFIG
        self.emotion_weight = self.config['emotion_weight']
        self.behavior_weight = self.config['behavior_weight']
        self.video_weight = self.config['video_weight']
        self.temporal_window = self.config['temporal_window']
        self.threshold = self.config['confusion_threshold']
        
        # History for temporal smoothing (moving average)
        self.score_history = deque(maxlen=self.temporal_window)
        
        print(f"[FusionEngine] Initialized with weights: "
              f"emotion={self.emotion_weight}, behavior={self.behavior_weight}, "
              f"video={self.video_weight}")
    
    def calculate_raw_score(self, emotion_score, behavior_score, video_score):
        """
        Calculate raw confusion score using weighted combination
        
        Formula:
        Confusion = 0.4 × Emotion + 0.3 × Behavior + 0.3 × Video
        
        Args:
            emotion_score: Emotion-based confusion score (0-1)
            behavior_score: Behavioral confusion score (0-1)
            video_score: Video interaction confusion score (0-1)
            
        Returns:
            float: Raw confusion score (0-1)
        """
        raw_score = (
            self.emotion_weight * emotion_score +
            self.behavior_weight * behavior_score +
            self.video_weight * video_score
        )
        
        return min(max(raw_score, 0.0), 1.0)  # Clamp to [0, 1]
    
    def apply_temporal_smoothing(self, raw_score):
        """
        Apply moving average to reduce noise and false positives
        
        Args:
            raw_score: Current raw confusion score
            
        Returns:
            float: Smoothed confusion score
        """
        # Add current score to history
        self.score_history.append(raw_score)
        
        # Calculate moving average
        if len(self.score_history) > 0:
            smoothed_score = sum(self.score_history) / len(self.score_history)
        else:
            smoothed_score = raw_score
        
        return smoothed_score
    
    def check_intervention_needed(self, smoothed_score):
        """
        Determine if intervention should be triggered
        
        Args:
            smoothed_score: Smoothed confusion score
            
        Returns:
            bool: True if intervention needed
        """
        return smoothed_score >= self.threshold
    
    def explain_confusion(self, emotion_score, behavior_score, video_score, 
                         smoothed_score):
        """
        Generate human-readable explanation for confusion detection
        
        Args:
            emotion_score: Emotion confusion score
            behavior_score: Behavioral confusion score
            video_score: Video interaction confusion score
            smoothed_score: Final smoothed score
            
        Returns:
            dict: Explanation with primary and contributing factors
        """
        # Identify primary confusion source
        scores = {
            'emotion': emotion_score,
            'behavior': behavior_score,
            'video': video_score
        }
        
        primary_source = max(scores, key=scores.get)
        primary_score = scores[primary_source]
        
        # Generate explanation
        explanations = {
            'emotion': 'Facial expressions indicate confusion or frustration',
            'behavior': 'Mouse and keyboard activity shows hesitation patterns',
            'video': 'Frequent pausing and rewinding detected'
        }
        
        # Find contributing factors (scores > 0.5)
        contributing = [
            source for source, score in scores.items() 
            if score > 0.5 and source != primary_source
        ]
        
        return {
            'primary_factor': primary_source,
            'primary_score': round(primary_score, 3),
            'primary_explanation': explanations[primary_source],
            'contributing_factors': contributing,
            'overall_confidence': round(smoothed_score, 3)
        }
    
    def fuse_scores(self, emotion_score, behavior_score, video_score):
        """
        Complete fusion pipeline: combine -> smooth -> decide -> explain
        
        Args:
            emotion_score: Emotion-based confusion score
            behavior_score: Behavioral confusion score
            video_score: Video interaction confusion score
            
        Returns:
            dict: Complete fusion result with decision and explanation
        """
        # Step 1: Calculate raw weighted score
        raw_score = self.calculate_raw_score(
            emotion_score, behavior_score, video_score
        )
        
        # Step 2: Apply temporal smoothing
        smoothed_score = self.apply_temporal_smoothing(raw_score)
        
        # Step 3: Check if intervention needed
        intervention_needed = self.check_intervention_needed(smoothed_score)
        
        # Step 4: Generate explanation
        explanation = self.explain_confusion(
            emotion_score, behavior_score, video_score, smoothed_score
        )
        
        return {
            'success': True,
            'raw_score': round(raw_score, 3),
            'smoothed_score': round(smoothed_score, 3),
            'intervention_needed': intervention_needed,
            'threshold': self.threshold,
            'component_scores': {
                'emotion': round(emotion_score, 3),
                'behavior': round(behavior_score, 3),
                'video': round(video_score, 3)
            },
            'explanation': explanation,
            'timestamp': datetime.now().isoformat()
        }
    
    def reset_history(self):
        """Reset temporal smoothing history (e.g., new session)"""
        self.score_history.clear()
        print("[FusionEngine] History reset")


# Singleton instance
fusion_engine = ConfusionFusionEngine()


def fuse_confusion_scores(emotion_score, behavior_score, video_score):
    """
    Public API function for confusion score fusion
    
    Args:
        emotion_score: Emotion confusion score (0-1)
        behavior_score: Behavioral confusion score (0-1)
        video_score: Video interaction confusion score (0-1)
        
    Returns:
        dict: Fusion result with intervention decision and explanation
    """
    return fusion_engine.fuse_scores(emotion_score, behavior_score, video_score)


def reset_fusion_history():
    """Reset fusion engine history"""
    fusion_engine.reset_history()
