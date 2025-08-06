import requests
import json

# Test the Flask API directly
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
    response = requests.post('http://127.0.0.1:5000/predict', json=test_data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)
