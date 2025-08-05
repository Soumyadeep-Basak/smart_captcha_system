from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from keras.losses import MeanSquaredError
import json
import os

app = Flask(__name__)
CORS(app)

# Instead of MongoDB, use local JSON file for storage
PREDICTIONS_FILE = 'predictions.json'

# Load the autoencoder model and scaler
try:
    autoencoder = load_model('autoencoder_model.h5', custom_objects={'mse': MeanSquaredError()})
    scaler = joblib.load('scaler.pkl')
    print("ML Model loaded successfully!")
except Exception as e:
    print(f"Error loading ML model: {e}")
    autoencoder = None
    scaler = None

class FeatureExtractor:
    def transform(self, X):
        df = pd.DataFrame(X, columns=['timestamp', 'x_position', 'y_position', 'event_name'])

        # Drop the 'event_name' as it's not needed
        df = df.drop(columns=['event_name'])

        # Handle missing positions
        df.loc[(df['x_position'] == 0) & (df['y_position'] == 0), ['x_position', 'y_position']] = np.nan
        df[['x_position', 'y_position']] = df[['x_position', 'y_position']].ffill()

        df['time_diff'] = df['timestamp'].diff().fillna(0)
        df['distance'] = np.sqrt((df['x_position'].diff())**2 + (df['y_position'].diff())**2).fillna(0)
        df['speed'] = df['distance'] / df['time_diff'].replace(0, np.nan)
        df['acceleration'] = df['speed'].diff() / df['time_diff'].replace(0, np.nan)
        df.fillna(0, inplace=True)

        def compute_angle_diff(x1, y1, x2, y2):
            angle = np.arctan2(y2 - y1, x2 - x1)
            return np.degrees(angle)

        df['angle_diff'] = compute_angle_diff(df['x_position'].shift(1), df['y_position'].shift(1),
                                              df['x_position'], df['y_position']).fillna(0)

        summary = pd.DataFrame({
            'speed_mean': [df['speed'].mean()],
            'speed_std': [df['speed'].std()],
            'acceleration_mean': [df['acceleration'].mean()],
            'acceleration_std': [df['acceleration'].std()],
            'angle_diff_mean': [df['angle_diff'].mean()],
            'angle_diff_std': [df['angle_diff'].std()]
        })

        return summary

class AutoencoderPredictor:
    def __init__(self, model, threshold=300):  # Changed to 300 for inverted logic
        self.model = model
        self.threshold = threshold

    def transform(self, X):
        if self.model is None:
            print("WARNING: ML model not available - using fallback detection")
            # Fallback if model fails to load
            return pd.DataFrame([{
                'bot': True,  # Assume bot if model fails
                'reconstruction_error': 0.9
            }])
        
        try:
            print(f"Running ML prediction on {X.shape} features...")
            # Get predictions from the autoencoder
            predictions = self.model.predict(X, verbose=0)
            print(f"Autoencoder output shape: {predictions.shape}")
            
            # Calculate reconstruction error
            reconstruction_errors = np.mean(np.square(X - predictions), axis=1)
            
            # PROCESSING FOR DISPLAY: Standardize and invert reconstruction errors
            # Step 1: Standardize to 0-1 range using 1500 as max threshold
            max_threshold = 1500.0
            standardized_errors = np.clip(reconstruction_errors / max_threshold, 0, 1)
            
            # Step 2: Invert the values (1 - standardized_value)
            display_errors = 1.0 - standardized_errors
            
            print(f"Processed display errors: {display_errors}")
            
            # Determine if it's a bot based on reconstruction error (INVERTED LOGIC)
            # Model was trained opposite way: error < 300 = bot, error >= 300 = human
            is_bot = reconstruction_errors < self.threshold
            print(f"Bot detection threshold: {self.threshold}")
            print(f"Bot detection results: {is_bot}")
            
            results = []
            for i in range(len(reconstruction_errors)):
                results.append({
                    'bot': bool(is_bot[i]),
                    'reconstruction_error': float(display_errors[i])  # Use processed display error
                })
            
            print(f"ML prediction complete: {results}")
            return pd.DataFrame(results)
            
        except Exception as e:
            print(f"ML prediction error: {e}")
            # Return high reconstruction error if prediction fails
            return pd.DataFrame([{
                'bot': True,
                'reconstruction_error': 0.95
            }])

# Initialize feature extractor and predictor
feature_extractor = FeatureExtractor()
autoencoder_predictor = AutoencoderPredictor(autoencoder) if autoencoder else None

def save_prediction(data):
    """Save prediction to JSON file instead of MongoDB"""
    try:
        # Load existing predictions
        if os.path.exists(PREDICTIONS_FILE):
            with open(PREDICTIONS_FILE, 'r') as f:
                predictions = json.load(f)
        else:
            predictions = []
        
        # Add new prediction
        predictions.append(data)
        
        # Save back to file
        with open(PREDICTIONS_FILE, 'w') as f:
            json.dump(predictions, f, indent=2)
        
        print(f"Prediction saved to {PREDICTIONS_FILE}")
    except Exception as e:
        print(f"Error saving prediction: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Incoming data:", data)
        
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        # Ensure required fields exist
        if 'mouseMoveCount' not in data or 'keyPressCount' not in data:
            return jsonify({"error": "mouseMoveCount and keyPressCount are required"}), 400
        
        mouse_move_count = data.get('mouseMoveCount')
        key_press_count = data.get('keyPressCount')
        input_data = data['events']
        
        # Convert to DataFrame
        input_df = pd.DataFrame(input_data)
        
        # Validate input
        required_columns = ['timestamp', 'x_position', 'y_position']
        if not all(col in input_df.columns for col in required_columns):
            return jsonify({"error": "Invalid input format"}), 400
        
        if autoencoder_predictor is None:
            return jsonify({"error": "ML model not available"}), 500
        
        # Extract features
        features = feature_extractor.transform(input_df)
        print("Extracted features:", features.to_dict())
        
        # Scale features
        scaled_features = scaler.transform(features)
        print("Scaled features shape:", scaled_features.shape)
        
        # Make predictions
        result = autoencoder_predictor.transform(scaled_features)
        print("ML Prediction:", result.to_dict())
        
        current_timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Create response
        response = {
            'ip_address': client_ip,
            'user_agent': user_agent,
            'current_timestamp': current_timestamp,
            'mouseMoveCount': mouse_move_count,
            'keyPressCount': key_press_count,
            'prediction': result.to_dict(orient='records')
        }
        
        # Save prediction to JSON file instead of MongoDB
        db_record = {
            'ip_address': client_ip,
            'user_agent': user_agent,
            'timestamp': current_timestamp,
            'input_data': input_data,
            'mouseMoveCount': mouse_move_count,
            'keyPressCount': key_press_count,
            'prediction': result.to_dict(orient='records')
        }
        save_prediction(db_record)
        
        print("Response:", response)
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in predict: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/predictions', methods=['GET'])
def get_predictions():
    """Get all predictions from JSON file"""
    try:
        if os.path.exists(PREDICTIONS_FILE):
            with open(PREDICTIONS_FILE, 'r') as f:
                predictions = json.load(f)
            return jsonify(predictions), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("Starting ML-based Flask server without MongoDB...")
    print(f"Predictions will be saved to: {PREDICTIONS_FILE}")
    app.run(debug=True, host='0.0.0.0', port=5000)
