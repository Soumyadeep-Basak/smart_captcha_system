from flask import Flask, request, jsonify
from flask_cors import CORS

import joblib
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from keras.losses import MeanSquaredError

app = Flask(__name__)
CORS(app)


autoencoder = load_model('autoencoder_model.h5',custom_objects={'mse': MeanSquaredError()})
scaler = joblib.load('scaler.pkl')

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
            'angle_diff_std': [df['angle_diff'].std()],
        })

        return summary


class AutoencoderPredictor:
    def __init__(self, model, threshold=200):
        self.model = model
        self.threshold = threshold

    def transform(self, X):
        y_reconstructed = self.model.predict(X)
        reconstruction_error = np.mean(np.square(X - y_reconstructed), axis=1)
        is_bot = reconstruction_error < self.threshold

        return pd.DataFrame({
            'reconstruction_error': reconstruction_error,
            'bot': is_bot
        })

# Create the pipeline
feature_extractor = FeatureExtractor()
autoencoder_predictor = AutoencoderPredictor(autoencoder)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse the incoming JSON request
        data = request.json
        
        # Convert JSON to DataFrame
        input_df = pd.DataFrame(data)
        
        # Validate input
        required_columns = ['timestamp', 'x_position', 'y_position']
        if not all(col in input_df.columns for col in required_columns):
            return jsonify({"error": "Invalid input format"}), 400
        
        # Extract features
        features = feature_extractor.transform(input_df)

        # Scale the features
        scaled_features = scaler.transform(features)

        # Make predictions
        result = autoencoder_predictor.transform(scaled_features)

        return jsonify(result.to_dict(orient='records'))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
