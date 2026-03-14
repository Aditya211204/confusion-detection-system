"""
Unit Tests for Confusion Fusion Engine
Tests score fusion, temporal smoothing, and intervention triggering
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.models.fusion_engine import ConfusionFusionEngine, fuse_confusion_scores, reset_fusion_history


class TestConfusionFusion(unittest.TestCase):
    """Test cases for confusion fusion engine"""
    
    def setUp(self):
        """Reset fusion history before each test"""
        reset_fusion_history()
        self.engine = ConfusionFusionEngine()
    
    def test_engine_initialization(self):
        """Test that fusion engine initializes correctly"""
        self.assertIsNotNone(self.engine)
        self.assertEqual(self.engine.emotion_weight, 0.4)
        self.assertEqual(self.engine.behavior_weight, 0.3)
        self.assertEqual(self.engine.video_weight, 0.3)
    
    def test_raw_score_calculation(self):
        """Test weighted score calculation"""
        emotion_score = 0.8
        behavior_score = 0.6
        video_score = 0.5
        
        raw_score = self.engine.calculate_raw_score(emotion_score, behavior_score, video_score)
        
        # Expected: 0.4*0.8 + 0.3*0.6 + 0.3*0.5 = 0.32 + 0.18 + 0.15 = 0.65
        expected = 0.65
        self.assertAlmostEqual(raw_score, expected, places=2)
    
    def test_temporal_smoothing(self):
        """Test moving average smoothing"""
        # Add multiple scores
        scores = [0.8, 0.7, 0.9, 0.6, 0.8]
        
        for score in scores:
            smoothed = self.engine.apply_temporal_smoothing(score)
        
        # Final smoothed score should be average of last 5 scores
        expected_avg = sum(scores) / len(scores)
        self.assertAlmostEqual(smoothed, expected_avg, places=2)
    
    def test_intervention_threshold(self):
        """Test intervention triggering at threshold"""
        # Score above threshold (0.6)
        high_score = 0.7
        self.assertTrue(self.engine.check_intervention_needed(high_score))
        
        # Score below threshold
        low_score = 0.5
        self.assertFalse(self.engine.check_intervention_needed(low_score))
    
    def test_complete_fusion_pipeline(self):
        """Test complete fusion process"""
        result = fuse_confusion_scores(0.7, 0.6, 0.5)
        
        # Check result structure
        self.assertTrue(result['success'])
        self.assertIn('raw_score', result)
        self.assertIn('smoothed_score', result)
        self.assertIn('intervention_needed', result)
        self.assertIn('explanation', result)
        
        # Check score ranges
        self.assertGreaterEqual(result['raw_score'], 0.0)
        self.assertLessEqual(result['raw_score'], 1.0)
    
    def test_explanation_generation(self):
        """Test confusion explanation generation"""
        emotion_score = 0.8
        behavior_score = 0.4
        video_score = 0.3
        
        explanation = self.engine.explain_confusion(
            emotion_score, behavior_score, video_score, 0.6
        )
        
        # Primary factor should be emotion (highest score)
        self.assertEqual(explanation['primary_factor'], 'emotion')
        self.assertEqual(explanation['primary_score'], 0.8)
        self.assertIn('primary_explanation', explanation)
    
    def test_score_clamping(self):
        """Test that scores are clamped to [0, 1]"""
        # Test with values that might exceed 1.0
        result = fuse_confusion_scores(1.0, 1.0, 1.0)
        
        self.assertLessEqual(result['raw_score'], 1.0)
        self.assertGreaterEqual(result['raw_score'], 0.0)


if __name__ == '__main__':
    print("=" * 60)
    print("Running Confusion Fusion Tests")
    print("=" * 60)
    unittest.main(verbosity=2)
