import requests
import json

# Test data to send to the Flask server
test_data = {
    "mouseMoveCount": 10,
    "keyPressCount": 5,
    "events": [
        {"timestamp": 1234567890, "x_position": 100, "y_position": 200, "event_name": "mousemove"},
        {"timestamp": 1234567891, "x_position": 110, "y_position": 210, "event_name": "mousemove"},
        {"timestamp": 1234567892, "x_position": 120, "y_position": 220, "event_name": "click"}
    ]
}

try:
    response = requests.post('http://127.0.0.1:5000/predict', 
                           json=test_data, 
                           headers={'Content-Type': 'application/json'})
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.ConnectionError:
    print("ERROR: Flask server is not running on port 5000")
except Exception as e:
    print("ERROR:", str(e))
