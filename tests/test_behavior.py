"""
Unit Tests for Behavioral Analysis Module
Tests mouse, keyboard, and video behavior analysis
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.models.behavior_model import BehaviorAnalyzer, analyze_behavior


class TestBehavioralAnalysis(unittest.TestCase):
    """Test cases for behavioral analysis module"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.analyzer = BehaviorAnalyzer()
    
    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly"""
        self.assertIsNotNone(self.analyzer)
        self.assertIsNotNone(self.analyzer.config)
    
    def test_mouse_behavior_analysis(self):
        """Test mouse behavior confusion detection"""
        # Test with high inactivity (should indicate confusion)
        high_inactivity_data = {
            'inactivity_duration': 35,  # Above threshold (30s)
            'movement_count': 2,
            'hesitation_count': 6  # Above threshold (5)
        }
        
        score = self.analyzer.analyze_mouse_behavior(high_inactivity_data)
        
        # Should return high confusion score
        self.assertGreater(score, 0.5)
        self.assertLessEqual(score, 1.0)
    
    def test_keyboard_behavior_analysis(self):
        """Test keyboard behavior confusion detection"""
        # Test with long pause and low typing speed
        confused_typing_data = {
            'pause_duration': 20,  # Above threshold (15s)
            'typing_speed': 10,    # Below threshold (20 cpm)
            'deletion_count': 8    # High deletions
        }
        
        score = self.analyzer.analyze_keyboard_behavior(confused_typing_data)
        
        # Should return high confusion score
        self.assertGreater(score, 0.5)
        self.assertLessEqual(score, 1.0)
    
    def test_video_behavior_analysis(self):
        """Test video interaction confusion detection"""
        # Test with frequent pausing and rewinding
        confused_video_data = {
            'pause_count': 6,   # Above threshold (5)
            'rewind_count': 4,  # Above threshold (3)
            'replay_count': 3   # Above threshold (2)
        }
        
        score = self.analyzer.analyze_video_behavior(confused_video_data)
        
        # Should return high confusion score
        self.assertGreater(score, 0.5)
        self.assertLessEqual(score, 1.0)
    
    def test_overall_behavior_score(self):
        """Test combined behavioral score calculation"""
        mouse_data = {'inactivity_duration': 25, 'movement_count': 3, 'hesitation_count': 4}
        keyboard_data = {'pause_duration': 18, 'typing_speed': 12, 'deletion_count': 6}
        video_data = {'pause_count': 5, 'rewind_count': 3, 'replay_count': 2}
        
        result = analyze_behavior(mouse_data, keyboard_data, video_data)
        
        # Check result structure
        self.assertTrue(result['success'])
        self.assertIn('overall_behavior_score', result)
        self.assertIn('mouse_score', result)
        self.assertIn('keyboard_score', result)
        self.assertIn('video_score', result)
        
        # Check score ranges
        self.assertGreaterEqual(result['overall_behavior_score'], 0.0)
        self.assertLessEqual(result['overall_behavior_score'], 1.0)
    
    def test_normal_behavior(self):
        """Test that normal behavior returns low confusion score"""
        normal_mouse = {'inactivity_duration': 5, 'movement_count': 20, 'hesitation_count': 1}
        normal_keyboard = {'pause_duration': 3, 'typing_speed': 50, 'deletion_count': 2}
        normal_video = {'pause_count': 1, 'rewind_count': 0, 'replay_count': 0}
        
        result = analyze_behavior(normal_mouse, normal_keyboard, normal_video)
        
        # Normal behavior should have low confusion score
        self.assertLess(result['overall_behavior_score'], 0.5)


if __name__ == '__main__':
    print("=" * 60)
    print("Running Behavioral Analysis Tests")
    print("=" * 60)
    unittest.main(verbosity=2)
