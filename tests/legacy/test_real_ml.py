import subprocess
import time
import requests
import json

print("🚀 Starting ML Flask Server Test...")

# Test if server is already running
try:
    response = requests.get('http://127.0.0.1:5000/', timeout=2)
    print("✅ Server is already running!")
except:
    print("❌ Server not running - will start it")

# Test the predict endpoint
test_data = {
    "mouseMoveCount": 2,  # Very low mouse movement (bot-like)
    "keyPressCount": 25,  # High key presses
    "events": [
        {"timestamp": 1000, "x_position": 100, "y_position": 100, "event_name": "click"},
        {"timestamp": 1010, "x_position": 200, "y_position": 200, "event_name": "click"},  # Exactly 10ms apart (bot-like)
        {"timestamp": 1020, "x_position": 300, "y_position": 300, "event_name": "click"},  # Exactly 10ms apart (bot-like)
        {"timestamp": 1030, "x_position": 400, "y_position": 400, "event_name": "click"},  # Exactly 10ms apart (bot-like)
        {"timestamp": 1040, "x_position": 500, "y_position": 500, "event_name": "click"},  # Exactly 10ms apart (bot-like)
        {"timestamp": 1050, "x_position": 600, "y_position": 600, "event_name": "click"},  # Exactly 10ms apart (bot-like)
    ]
}

try:
    print("🧪 Testing ML API...")
    response = requests.post('http://127.0.0.1:5000/predict', json=test_data, timeout=10)
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ ML API Response:")
        print(json.dumps(result, indent=2))
        
        # Check if it's using real ML model
        if 'prediction' in result:
            prediction = result['prediction'][0]
            reconstruction_error = prediction.get('reconstruction_error', 0)
            is_bot = prediction.get('bot', False)
            
            print(f"\n🔍 Analysis:")
            print(f"   Is Bot: {is_bot}")
            print(f"   Reconstruction Error: {reconstruction_error}")
            
            if reconstruction_error != 0.1:
                print("✅ REAL ML MODEL IS WORKING! (Non-default reconstruction error)")
            else:
                print("❌ Still using fallback logic (reconstruction error = 0.1)")
        else:
            print("❌ Invalid response format")
    else:
        print(f"❌ API Error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Flask server is not running on port 5000")
    print("🔧 Please run: start_ml_no_mongo.bat")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

print("\n🏁 Test complete!")
