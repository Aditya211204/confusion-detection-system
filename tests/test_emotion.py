"""
Unit Tests for Emotion Detection Module
Tests emotion recognition functionality and confusion score calculation
"""

import unittest
import sys
import os
import base64
from io import BytesIO
from PIL import Image
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.models.emotion_model import EmotionDetector, analyze_emotion


class TestEmotionDetection(unittest.TestCase):
    """Test cases for emotion detection module"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.detector = EmotionDetector()
    
    def create_test_image(self):
        """Create a simple test image"""
        # Create a blank image (100x100 RGB)
        img = Image.new('RGB', (100, 100), color='white')
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{img_str}"
    
    def test_detector_initialization(self):
        """Test that detector initializes correctly"""
        self.assertIsNotNone(self.detector)
        self.assertIsNotNone(self.detector.detector)
    
    def test_image_decoding(self):
        """Test base64 image decoding"""
        test_image = self.create_test_image()
        decoded = self.detector.decode_image(test_image)
        
        self.assertIsNotNone(decoded)
        self.assertIsInstance(decoded, np.ndarray)
    
    def test_confusion_score_calculation(self):
        """Test confusion score calculation from emotions"""
        test_emotions = {
            'angry': 0.1,
            'disgust': 0.05,
            'fear': 0.2,
            'happy': 0.3,
            'sad': 0.25,
            'surprise': 0.05,
            'neutral': 0.05
        }
        
        score = self.detector.calculate_confusion_score(test_emotions)
        
        # Score should be between 0 and 1
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        
        # With these emotions, score should be positive (sad and fear present)
        self.assertGreater(score, 0.0)
    
    def test_no_face_detected(self):
        """Test handling when no face is detected"""
        test_image = self.create_test_image()
        result = analyze_emotion(test_image)
        
        # Should return a result even if no face detected
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('confusion_score', result)
    
    def test_confusion_score_range(self):
        """Test that confusion scores are always in valid range"""
        # Test with extreme emotion values
        extreme_emotions = {
            'angry': 1.0,
            'disgust': 1.0,
            'fear': 1.0,
            'happy': 0.0,
            'sad': 1.0,
            'surprise': 0.0,
            'neutral': 0.0
        }
        
        score = self.detector.calculate_confusion_score(extreme_emotions)
        
        # Even with extreme values, score should be clamped to [0, 1]
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


if __name__ == '__main__':
    print("=" * 60)
    print("Running Emotion Detection Tests")
    print("=" * 60)
    unittest.main(verbosity=2)
