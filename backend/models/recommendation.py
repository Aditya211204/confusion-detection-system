"""
Recommendation Engine
Generates intelligent intervention suggestions based on confusion type
Implements adaptive learning from user feedback
Tracks recommendation effectiveness
"""

import sys
import os
from datetime import datetime
from collections import defaultdict

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RECOMMENDATION_CONFIG


class RecommendationEngine:
    """
    Generates adaptive recommendations for confused students
    Learns from feedback to improve future suggestions
    """
    
    def __init__(self):
        """Initialize recommendation engine with feedback tracking"""
        self.config = RECOMMENDATION_CONFIG
        self.intervention_types = self.config['intervention_types']
        self.learning_rate = self.config['feedback_learning_rate']
        
        # Track feedback for adaptive learning
        # Structure: {intervention_type: {'helpful': count, 'dismissed': count}}
        self.feedback_stats = defaultdict(lambda: {'helpful': 0, 'dismissed': 0})
        
        # Track last intervention time for cooldown
        self.last_intervention_time = None
        
        print("[RecommendationEngine] Initialized successfully")
    
    def get_rule_based_recommendation(self, primary_factor):
        """
        Get initial recommendation based on confusion source
        
        Rules:
        - Emotion-based confusion → Simpler explanation
        - Behavior-based confusion → Real-life example
        - Video-based confusion → Concept recap
        - Mixed confusion → Short quiz
        
        Args:
            primary_factor: Primary confusion source ('emotion', 'behavior', 'video')
            
        Returns:
            str: Recommended intervention type
        """
        rules = {
            'emotion': 'simpler_explanation',
            'behavior': 'real_life_example',
            'video': 'concept_recap'
        }
        
        return rules.get(primary_factor, 'short_quiz')
    
    def get_adaptive_recommendation(self, primary_factor):
        """
        Get recommendation with adaptive learning from feedback
        
        Selects intervention type with highest success rate for this confusion type
        Falls back to rule-based if insufficient feedback data
        
        Args:
            primary_factor: Primary confusion source
            
        Returns:
            str: Recommended intervention type
        """
        # Get rule-based baseline
        baseline_recommendation = self.get_rule_based_recommendation(primary_factor)
        
        # Calculate success rates for all intervention types
        success_rates = {}
        for intervention_type in self.intervention_types:
            stats = self.feedback_stats[intervention_type]
            total = stats['helpful'] + stats['dismissed']
            
            if total > 0:
                success_rate = stats['helpful'] / total
                success_rates[intervention_type] = success_rate
        
        # If we have enough feedback data, use best performing intervention
        if success_rates:
            best_intervention = max(success_rates, key=success_rates.get)
            best_rate = success_rates[best_intervention]
            
            # Only use adaptive if significantly better than baseline
            if best_rate > 0.6:  # 60% success threshold
                return best_intervention
        
        # Fall back to rule-based
        return baseline_recommendation
    
    def generate_intervention_content(self, intervention_type, topic="this concept"):
        """
        Generate content for intervention popup
        
        Args:
            intervention_type: Type of intervention
            topic: Current learning topic (default placeholder)
            
        Returns:
            dict: Intervention title, message, and action
        """
        content = {
            'simpler_explanation': {
                'title': '💡 Need a Simpler Explanation?',
                'message': f'It looks like {topic} might be confusing. Would you like a simplified breakdown?',
                'action': 'Show Simpler Explanation',
                'icon': '💡'
            },
            'real_life_example': {
                'title': '🌟 Real-Life Example',
                'message': f'Understanding {topic} better with a real-world example might help!',
                'action': 'Show Example',
                'icon': '🌟'
            },
            'short_quiz': {
                'title': '✅ Quick Knowledge Check',
                'message': 'Let\'s test your understanding with a quick quiz to clarify concepts.',
                'action': 'Start Quiz',
                'icon': '✅'
            },
            'concept_recap': {
                'title': '🔄 Concept Recap',
                'message': f'Let\'s quickly review the key points of {topic} together.',
                'action': 'Show Recap',
                'icon': '🔄'
            }
        }
        
        return content.get(intervention_type, content['simpler_explanation'])
    
    def check_cooldown(self):
        """
        Check if cooldown period has passed since last intervention
        
        Returns:
            bool: True if cooldown passed, False otherwise
        """
        if self.last_intervention_time is None:
            return True
        
        current_time = datetime.now()
        time_diff = (current_time - self.last_intervention_time).total_seconds()
        
        return time_diff >= self.config['cooldown_period']
    
    def generate_recommendation(self, confusion_data, use_adaptive=True):
        """
        Generate complete recommendation with cooldown check
        
        Args:
            confusion_data: Fusion engine output with explanation
            use_adaptive: Whether to use adaptive learning (default True)
            
        Returns:
            dict: Recommendation with intervention details or cooldown message
        """
        # Check cooldown
        if not self.check_cooldown():
            return {
                'success': True,
                'show_intervention': False,
                'reason': 'cooldown_active',
                'cooldown_remaining': self.config['cooldown_period']
            }
        
        # Get primary confusion factor
        primary_factor = confusion_data['explanation']['primary_factor']
        
        # Select intervention type
        if use_adaptive:
            intervention_type = self.get_adaptive_recommendation(primary_factor)
        else:
            intervention_type = self.get_rule_based_recommendation(primary_factor)
        
        # Generate intervention content
        content = self.generate_intervention_content(intervention_type)
        
        # Update last intervention time
        self.last_intervention_time = datetime.now()
        
        return {
            'success': True,
            'show_intervention': True,
            'intervention_type': intervention_type,
            'content': content,
            'confusion_explanation': confusion_data['explanation'],
            'timestamp': datetime.now().isoformat()
        }
    
    def record_feedback(self, intervention_type, was_helpful):
        """
        Record user feedback for adaptive learning
        
        Args:
            intervention_type: Type of intervention shown
            was_helpful: Boolean indicating if user found it helpful
        """
        if was_helpful:
            self.feedback_stats[intervention_type]['helpful'] += 1
        else:
            self.feedback_stats[intervention_type]['dismissed'] += 1
        
        print(f"[RecommendationEngine] Feedback recorded: {intervention_type} - "
              f"{'helpful' if was_helpful else 'dismissed'}")
    
    def get_feedback_stats(self):
        """
        Get current feedback statistics
        
        Returns:
            dict: Feedback statistics for all intervention types
        """
        stats = {}
        for intervention_type in self.intervention_types:
            data = self.feedback_stats[intervention_type]
            total = data['helpful'] + data['dismissed']
            success_rate = data['helpful'] / total if total > 0 else 0
            
            stats[intervention_type] = {
                'helpful': data['helpful'],
                'dismissed': data['dismissed'],
                'total': total,
                'success_rate': round(success_rate, 3)
            }
        
        return stats


# Singleton instance
recommendation_engine = RecommendationEngine()


def generate_recommendation(confusion_data, use_adaptive=True):
    """
    Public API function for generating recommendations
    
    Args:
        confusion_data: Confusion fusion result
        use_adaptive: Use adaptive learning (default True)
        
    Returns:
        dict: Recommendation with intervention details
    """
    return recommendation_engine.generate_recommendation(confusion_data, use_adaptive)


def record_feedback(intervention_type, was_helpful):
    """
    Public API function for recording feedback
    
    Args:
        intervention_type: Type of intervention
        was_helpful: Whether user found it helpful
    """
    recommendation_engine.record_feedback(intervention_type, was_helpful)


def get_feedback_stats():
    """Get feedback statistics"""
    return recommendation_engine.get_feedback_stats()
