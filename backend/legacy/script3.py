from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Simple bot detection without ML model for now
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Received data:", data)
        
        # Extract the data in the format the FormComponent sends
        mouse_move_count = data.get('mouseMoveCount', 0)
        key_press_count = data.get('keyPressCount', 0) 
        events = data.get('events', [])
        
        print(f"Received: {len(events)} events, {mouse_move_count} mouse moves, {key_press_count} key presses")
        
        # Advanced bot detection logic
        is_bot = False
        reconstruction_error = 0.1  # Default low error
        
        if len(events) > 0:
            # Analyze patterns that might indicate bot behavior
            time_diffs = []
            for i in range(1, len(events)):
                time_diff = events[i]['timestamp'] - events[i-1]['timestamp']
                time_diffs.append(time_diff)
            
            if len(time_diffs) > 5:
                avg_time = sum(time_diffs) / len(time_diffs)
                variance = sum((x - avg_time) ** 2 for x in time_diffs) / len(time_diffs)
                
                # Bot detection criteria:
                # 1. Very consistent timing (low variance)
                # 2. Too fast movements
                # 3. Too many events in short time
                # 4. Perfect patterns
                
                if variance < 50:  # Very consistent timing
                    is_bot = True
                    reconstruction_error = 0.8
                    print("Bot detected: Very consistent timing patterns")
                elif avg_time < 5:  # Too fast
                    is_bot = True
                    reconstruction_error = 0.9
                    print("Bot detected: Too fast movements")
                elif len(events) > 100 and len(events) < 10:  # Suspicious event count
                    is_bot = True
                    reconstruction_error = 0.7
                    print("Bot detected: Suspicious event count")
                else:
                    print("Human-like behavior detected")
                    reconstruction_error = 0.1
        
        # Additional checks for very obvious bots
        if mouse_move_count < 5 and key_press_count > 20:  # Only typing, no mouse movement
            is_bot = True
            reconstruction_error = 0.95
            print("Bot detected: No mouse movement but high key presses")
        
        print(f"Final decision: is_bot={is_bot}, reconstruction_error={reconstruction_error}")
            
        # Mock response in the format the FormComponent expects
        response = {
            "ip_address": "127.0.0.1",
            "user_agent": "Test User Agent", 
            "current_timestamp": datetime.now().isoformat(),
            "prediction": [{"bot": is_bot, "reconstruction_error": reconstruction_error}]
        }
        
        print(f"Sending response: {response}")
        return jsonify(response)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  