"""
Simplified Emotion Recognition Module (OpenCV-based)
Uses face detection and simulated emotion scoring for demo purposes
Works without FER library dependency issues
"""

import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import sys
import os
import random

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import EMOTION_CONFIG


class EmotionDetector:
    """
    Simplified facial emotion recognition using OpenCV
    For demo purposes - simulates emotion detection
    """
    
    def __init__(self):
        """Initialize the detector with Haar Cascade"""
        try:
            # Load Haar Cascade for face detection
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            self.emotion_weights = EMOTION_CONFIG['confusion_emotions']
            self.confidence_threshold = EMOTION_CONFIG['confidence_threshold']
            print("[EmotionDetector] Initialized successfully (OpenCV-based)")
        except Exception as e:
            print(f"[EmotionDetector] Error initializing: {e}")
            self.face_cascade = None
    
    def decode_image(self, base64_string):
        """
        Decode base64 image string to numpy array
        
        Args:
            base64_string: Base64 encoded image from webcam
            
        Returns:
            numpy.ndarray: Decoded image in BGR format
        """
        try:
            # Remove data URL prefix if present
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64 to bytes
            image_bytes = base64.b64decode(base64_string)
            
            # Convert to PIL Image
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to numpy array (RGB)
            image_np = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            
            return image_bgr
        except Exception as e:
            print(f"[EmotionDetector] Error decoding image: {e}")
            return None
    
    def detect_emotions(self, image):
        """
        Detect face and simulate emotion probabilities
        
        Args:
            image: numpy.ndarray image in BGR format
            
        Returns:
            dict: Emotion probabilities and confusion score
        """
        if self.face_cascade is None:
            return {
                'success': False,
                'error': 'Detector not initialized',
                'emotions': {},
                'confusion_score': 0.0
            }
        
        try:
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) == 0:
                return {
                    'success': False,
                    'error': 'No face detected',
                    'emotions': {},
                    'confusion_score': 0.0
                }
            
            # Simulate emotion detection (for demo purposes)
            # In production, this would use a trained model
            emotions = self.simulate_emotions()
            
            # Calculate confusion score
            confusion_score = self.calculate_confusion_score(emotions)
            
            return {
                'success': True,
                'emotions': emotions,
                'confusion_score': confusion_score,
                'face_detected': True
            }
            
        except Exception as e:
            print(f"[EmotionDetector] Error detecting emotions: {e}")
            return {
                'success': False,
                'error': str(e),
                'emotions': {},
                'confusion_score': 0.0
            }
    
    def simulate_emotions(self):
        """
        Simulate emotion probabilities for demo
        In production, replace with actual ML model
        
        Returns:
            dict: Simulated emotion probabilities
        """
        # Generate realistic emotion distribution
        # Bias towards neutral/happy for normal state
        emotions = {
            'angry': random.uniform(0.0, 0.15),
            'disgust': random.uniform(0.0, 0.1),
            'fear': random.uniform(0.0, 0.2),
            'happy': random.uniform(0.2, 0.5),
            'sad': random.uniform(0.0, 0.25),
            'surprise': random.uniform(0.0, 0.15),
            'neutral': random.uniform(0.1, 0.4)
        }
        
        # Normalize to sum to 1.0
        total = sum(emotions.values())
        emotions = {k: v/total for k, v in emotions.items()}
        
        return emotions
    
    def calculate_confusion_score(self, emotions):
        """
        Calculate confusion score from emotion probabilities
        
        Confusion indicators:
        - High: sad (0.5), fear (0.4), angry (0.3)
        - Low: happy (-0.2), neutral (0.0)
        
        Args:
            emotions: dict of emotion probabilities
            
        Returns:
            float: Confusion score between 0 and 1
        """
        confusion_score = 0.0
        
        for emotion, probability in emotions.items():
            if emotion in self.emotion_weights:
                confusion_score += probability * self.emotion_weights[emotion]
        
        # Normalize to 0-1 range
        confusion_score = max(0.0, min(1.0, confusion_score))
        
        return confusion_score
    
    def process_frame(self, base64_image):
        """
        Complete pipeline: decode image -> detect emotions -> calculate score
        
        Args:
            base64_image: Base64 encoded image string
            
        Returns:
            dict: Complete emotion analysis result
        """
        # Decode image
        image = self.decode_image(base64_image)
        
        if image is None:
            return {
                'success': False,
                'error': 'Failed to decode image',
                'emotions': {},
                'confusion_score': 0.0
            }
        
        # Detect emotions
        result = self.detect_emotions(image)
        
        return result


# Singleton instance for reuse across requests
emotion_detector = EmotionDetector()


def analyze_emotion(base64_image):
    """
    Public API function for emotion analysis
    
    Args:
        base64_image: Base64 encoded image from webcam
        
    Returns:
        dict: Emotion analysis result with confusion score
    """
    return emotion_detector.process_frame(base64_image)
