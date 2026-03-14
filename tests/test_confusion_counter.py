"""
Test Confusion Counter - Verify session tracking works correctly
Tests that confusion events and interventions are tracked separately
"""

import requests
import json

API_BASE_URL = 'http://127.0.0.1:5000/api'

def test_confusion_counter():
    """Test that confusion counter tracks events correctly"""
    print("=" * 60)
    print("Testing Confusion Counter")
    print("=" * 60)
    
    # Test 1: Send multiple high confusion scores to build up temporal smoothing
    print("\n1. Building up temporal smoothing window (5 requests)...")
    for i in range(5):
        print(f"   Request {i+1}/5...")
        response = requests.post(
            f'{API_BASE_URL}/intervention/check',
            headers={'X-Session-ID': 'test-session-001'},
            json={
                'emotion_score': 0.8,
                'behavior_score': 0.7,
                'video_score': 0.6
            }
        )
        
        result = response.json()
        assert result['success'], "Request should succeed"
    
    # Now the smoothed score should be high enough to trigger intervention
    print("\n2. Testing high confusion scores (should trigger intervention)...")
    response = requests.post(
        f'{API_BASE_URL}/intervention/check',
        headers={'X-Session-ID': 'test-session-001'},
        json={
            'emotion_score': 0.8,
            'behavior_score': 0.7,
            'video_score': 0.6
        }
    )
    
    result = response.json()
    print(f"   Response: {json.dumps(result, indent=2)}")
    
    assert result['success'], "Request should succeed"
    assert result['intervention_needed'], "Intervention should be needed"
    
    session_stats = result.get('session_stats', {})
    print(f"\n   Session Stats: {session_stats}")
    
    # 6 confusion events (5 warmup + 1 test)
    # 1 intervention (only the last one triggers due to cooldown)
    expected_confusion = 6
    expected_interventions = 1
    
    assert session_stats['confusion_events'] == expected_confusion, \
        f"Expected {expected_confusion} confusion events, got {session_stats['confusion_events']}"
    assert session_stats['intervention_count'] == expected_interventions, \
        f"Expected {expected_interventions} interventions, got {session_stats['intervention_count']}"
    
    print("   ✅ Test passed!")
    
    # Test 2: High confusion but within cooldown (should trigger confusion but NOT intervention)
    print("\n3. Testing high confusion within cooldown (no intervention popup)...")
    response = requests.post(
        f'{API_BASE_URL}/intervention/check',
        headers={'X-Session-ID': 'test-session-001'},
        json={
            'emotion_score': 0.9,
            'behavior_score': 0.8,
            'video_score': 0.7
        }
    )
    
    result = response.json()
    print(f"   Response: {json.dumps(result, indent=2)}")
    
    assert result['success'], "Request should succeed"
    assert result['intervention_needed'], "Confusion should be detected"
    
    session_stats = result.get('session_stats', {})
    print(f"\n   Session Stats: {session_stats}")
    
    expected_confusion = 7  # Incremented (6 + 1)
    expected_interventions = 1  # NOT incremented (cooldown active)
    
    assert session_stats['confusion_events'] == expected_confusion, \
        f"Expected {expected_confusion} confusion events, got {session_stats['confusion_events']}"
    assert session_stats['intervention_count'] == expected_interventions, \
        f"Expected {expected_interventions} interventions, got {session_stats['intervention_count']}"
    
    print("   ✅ Test passed!")
    
    # Test 3: Low confusion scores (should NOT trigger anything)
    print("\n4. Testing low confusion scores (no confusion, no intervention)...")
    response = requests.post(
        f'{API_BASE_URL}/intervention/check',
        headers={'X-Session-ID': 'test-session-001'},
        json={
            'emotion_score': 0.2,
            'behavior_score': 0.1,
            'video_score': 0.15
        }
    )
    
    result = response.json()
    print(f"   Response: {json.dumps(result, indent=2)}")
    
    assert result['success'], "Request should succeed"
    assert not result['intervention_needed'], "Intervention should NOT be needed"
    
    session_stats = result.get('session_stats', {})
    print(f"\n   Session Stats: {session_stats}")
    
    expected_confusion = 7  # NOT incremented (no confusion)
    expected_interventions = 1  # NOT incremented
    
    assert session_stats['confusion_events'] == expected_confusion, \
        f"Expected {expected_confusion} confusion events, got {session_stats['confusion_events']}"
    assert session_stats['intervention_count'] == expected_interventions, \
        f"Expected {expected_interventions} interventions, got {session_stats['intervention_count']}"
    
    print("   ✅ Test passed!")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_confusion_counter()
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        exit(1)
    except requests.exceptions.ConnectionError:
        print("\nCould not connect to backend. Make sure the server is running.")
        print("   Run: python backend/app.py")
        exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        exit(1)
