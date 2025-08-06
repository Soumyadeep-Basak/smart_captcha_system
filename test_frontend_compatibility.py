#!/usr/bin/env python3
"""
Test the specific response format that frontend expects
"""

import requests
import json

# Test data - same format as frontend sends
test_data = {
    "mouseMoveCount": 15,
    "keyPressCount": 8,
    "events": [
        {"timestamp": 1000, "x_position": 100, "y_position": 200, "event_name": "mousemove"},
        {"timestamp": 1100, "x_position": 110, "y_position": 210, "event_name": "mousemove"},
        {"timestamp": 1200, "x_position": 120, "y_position": 220, "event_name": "mousemove"},
        {"timestamp": 1300, "x_position": 130, "y_position": 230, "event_name": "mousemove"},
        {"timestamp": 1400, "x_position": 140, "y_position": 240, "event_name": "mousemove"},
    ]
}

def test_frontend_compatibility():
    """Test that the response format matches what frontend expects"""
    try:
        print("🧪 Testing Frontend Compatibility...")
        print("=" * 50)
        
        # Send request to API Gateway
        response = requests.post("http://localhost:5000/predict", json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Gateway Response received!")
            
            # Check expected fields for frontend
            expected_fields = ['ip_address', 'user_agent', 'current_timestamp', 'prediction']
            missing_fields = []
            
            for field in expected_fields:
                if field in result:
                    print(f"  ✅ {field}: Present")
                else:
                    print(f"  ❌ {field}: MISSING")
                    missing_fields.append(field)
            
            # Check prediction array format
            if 'prediction' in result and isinstance(result['prediction'], list):
                if len(result['prediction']) > 0:
                    pred = result['prediction'][0]
                    print(f"  ✅ prediction[0]: {pred}")
                    
                    # Check prediction[0] fields
                    pred_fields = ['bot', 'reconstruction_error', 'confidence']
                    for field in pred_fields:
                        if field in pred:
                            print(f"    ✅ prediction[0].{field}: {pred[field]}")
                        else:
                            print(f"    ❌ prediction[0].{field}: MISSING")
                else:
                    print("  ❌ prediction array is empty!")
            else:
                print("  ❌ prediction is not an array!")
            
            print("\n🔍 Full Response Structure:")
            print("-" * 30)
            print(json.dumps(result, indent=2))
            
            if not missing_fields:
                print("\n🎉 Frontend compatibility: PERFECT!")
                return True
            else:
                print(f"\n❌ Frontend compatibility: FAILED - Missing {missing_fields}")
                return False
        
        else:
            print(f"❌ API Gateway Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = test_frontend_compatibility()
    
    if success:
        print("\n✅ The form submission should now work!")
    else:
        print("\n❌ Form submission will still fail - check the errors above")
