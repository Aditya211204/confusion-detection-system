"""
Run all tests for the confusion detection system
"""

import sys
import os
import unittest

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import test modules
from test_emotion import TestEmotionDetection
from test_behavior import TestBehavioralAnalysis
from test_fusion import TestConfusionFusion


def run_all_tests():
    """Run all test suites"""
    
    print("=" * 70)
    print("AI-Based Silent Confusion Detection System - Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestEmotionDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestBehavioralAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestConfusionFusion))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
