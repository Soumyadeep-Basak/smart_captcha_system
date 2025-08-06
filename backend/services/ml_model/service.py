# ML Model Service - TensorFlow Model Management
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib
import pandas as pd
import numpy as np
import json
import os
import sys
from pathlib import Path

# Add timeout and error handling for TensorFlow import
def safe_tensorflow_import():
    try:
        print("🔄 Loading TensorFlow (this may take a moment)...")
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
        import tensorflow as tf
        tf.get_logger().setLevel('ERROR')
        from tensorflow.keras.models import load_model
        from tensorflow.keras.losses import MeanSquaredError
        print("✅ TensorFlow loaded successfully!")
        return load_model, MeanSquaredError, True
    except ImportError as e:
        print(f"❌ TensorFlow import error: {e}")
        return None, None, False
    except Exception as e:
        print(f"❌ TensorFlow loading error: {e}")
        return None, None, False

# Import TensorFlow with error handling
load_model, MeanSquaredError, tf_available = safe_tensorflow_import()

app = Flask(__name__)
CORS(app)

# Path configuration for models
BASE_DIR = Path(__file__).parent.parent.parent
MODELS_DIR = BASE_DIR / 'models'
LOGS_DIR = BASE_DIR / 'logs' / 'predictions'

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
PREDICTIONS_FILE = LOGS_DIR / 'ml_predictions.json'

# Load the autoencoder model and scaler with better error handling
def load_ml_models():
    if not tf_available:
        print("⚠️ TensorFlow not available - ML service will run in fallback mode")
        return None, None
    
    try:
        model_path = MODELS_DIR / 'autoencoder' / 'autoencoder_model.h5'
        scaler_path = MODELS_DIR / 'autoencoder' / 'scaler.pkl'
        
        print(f"🔍 Looking for model at: {model_path}")
        print(f"🔍 Looking for scaler at: {scaler_path}")
        
        if not model_path.exists():
            print(f"❌ Model file not found: {model_path}")
            return None, None
        
        if not scaler_path.exists():
            print(f"❌ Scaler file not found: {scaler_path}")
            return None, None
        
        print("🔄 Loading autoencoder model...")
        autoencoder = load_model(str(model_path), custom_objects={'mse': MeanSquaredError()})
        
        print("🔄 Loading scaler...")
        scaler = joblib.load(str(scaler_path))
        
        print("✅ ML Model and scaler loaded successfully!")
        return autoencoder, scaler
        
    except Exception as e:
        print(f"❌ Error loading ML model: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return None, None

# Load models
print("🚀 Initializing ML Model Service...")
autoencoder, scaler = load_ml_models()

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
    def __init__(self, model, threshold=300):
        self.model = model
        self.threshold = threshold

    def transform(self, X):
        if self.model is None:
            print("⚠️ WARNING: ML model not available - using fallback detection")
            return pd.DataFrame([{
                'bot': True,
                'reconstruction_error': 0.9,
                'confidence': 0.5,
                'raw_error': 999.0,
                'threshold_used': self.threshold,
                'model_status': 'unavailable'
            }])
        
        try:
            print(f"🧠 Running ML prediction on {X.shape} features...")
            print(f"🔧 Input features shape: {X.shape}")
            print(f"🔧 Features being processed: {X}")
            
            predictions = self.model.predict(X, verbose=0)
            print(f"🔧 Model output shape: {predictions.shape}")
            print(f"🔧 Model predictions: {predictions}")
            
            # Calculate reconstruction error
            reconstruction_errors = np.mean(np.square(X - predictions), axis=1)
            print(f"🔢 Raw reconstruction errors: {reconstruction_errors}")
            print(f"🔢 Threshold being used: {self.threshold}")
            
            # Process for display: Standardize and invert reconstruction errors
            max_threshold = 1500.0
            standardized_errors = np.clip(reconstruction_errors / max_threshold, 0, 1)
            display_errors = 1.0 - standardized_errors
            
            print(f"🔢 Standardized errors (0-1): {standardized_errors}")
            print(f"🔢 Display errors (inverted): {display_errors}")
            
            # Bot detection with inverted logic
            is_bot = reconstruction_errors < self.threshold
            print(f"🤖 Bot detection results: {is_bot}")
            print(f"🤖 Logic: reconstruction_error < {self.threshold} = bot")
            
            results = []
            for i in range(len(reconstruction_errors)):
                raw_error = float(reconstruction_errors[i])
                display_error = float(display_errors[i])
                is_bot_decision = bool(is_bot[i])
                
                # Calculate confidence based on distance from threshold
                distance_from_threshold = abs(raw_error - self.threshold)
                confidence = min(distance_from_threshold / self.threshold, 1.0)
                
                result_item = {
                    'bot': is_bot_decision,
                    'reconstruction_error': display_error,  # For frontend compatibility
                    'confidence': min(confidence, 1.0),
                    'raw_error': raw_error,
                    'threshold_used': self.threshold,
                    'decision_logic': f"raw_error ({raw_error:.2f}) < threshold ({self.threshold}) = {is_bot_decision}",
                    'standardized_error': float(standardized_errors[i]),
                    'max_threshold': max_threshold,
                    'model_status': 'active'
                }
                
                results.append(result_item)
                
                # Detailed logging for each result
                print(f"📊 Result {i+1}:")
                print(f"   Raw Error: {raw_error:.4f}")
                print(f"   Threshold: {self.threshold}")
                print(f"   Bot Decision: {is_bot_decision} (because {raw_error:.2f} {'<' if is_bot_decision else '>='} {self.threshold})")
                print(f"   Display Error: {display_error:.4f}")
                print(f"   Confidence: {confidence:.4f}")
            
            print(f"✅ ML prediction complete: {len(results)} results processed")
            return pd.DataFrame(results)
            
        except Exception as e:
            print(f"❌ ML prediction error: {e}")
            import traceback
            print(f"❌ Full error traceback: {traceback.format_exc()}")
            return pd.DataFrame([{
                'bot': True,
                'reconstruction_error': 0.95,
                'confidence': 0.8,
                'raw_error': 999.0,
                'threshold_used': self.threshold,
                'decision_logic': f"error_fallback",
                'model_status': 'error'
            }])

# Initialize feature extractor and predictor
feature_extractor = FeatureExtractor()
autoencoder_predictor = AutoencoderPredictor(autoencoder) if autoencoder else None

def save_prediction(data):
    """Save prediction to JSON file"""
    try:
        if PREDICTIONS_FILE.exists():
            with open(PREDICTIONS_FILE, 'r') as f:
                predictions = json.load(f)
        else:
            predictions = []
        
        predictions.append(data)
        
        with open(PREDICTIONS_FILE, 'w') as f:
            json.dump(predictions, f, indent=2)
        
        print(f"💾 Prediction saved to {PREDICTIONS_FILE}")
    except Exception as e:
        print(f"❌ Error saving prediction: {e}")

@app.route('/health')
def health():
    model_status = "loaded" if autoencoder is not None else "failed"
    scaler_status = "loaded" if scaler is not None else "failed"
    
    return jsonify({
        'status': 'healthy',
        'service': 'ml_model',
        'model_status': model_status,
        'scaler_status': scaler_status,
        'predictions_file': str(PREDICTIONS_FILE)
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print(f"📥 Incoming ML prediction request")
        
        # Extract client info
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent')
        
        # Validate required fields
        if 'mouseMoveCount' not in data or 'keyPressCount' not in data:
            return jsonify({"error": "mouseMoveCount and keyPressCount are required"}), 400
        
        mouse_move_count = data.get('mouseMoveCount')
        key_press_count = data.get('keyPressCount')
        input_data = data['events']
        
        # Convert to DataFrame
        input_df = pd.DataFrame(input_data)
        
        # Validate input format
        required_columns = ['timestamp', 'x_position', 'y_position']
        if not all(col in input_df.columns for col in required_columns):
            return jsonify({"error": "Invalid input format - missing required columns"}), 400
        
        if autoencoder_predictor is None:
            return jsonify({"error": "ML model not available"}), 500
        
        # Extract features
        features = feature_extractor.transform(input_df)
        print(f"🔧 Extracted features: {features.shape}")
        
        # Scale features
        scaled_features = scaler.transform(features)
        print(f"📏 Scaled features: {scaled_features.shape}")
        
        # Make predictions
        result = autoencoder_predictor.transform(scaled_features)
        print(f"🎯 ML Prediction complete")
        
        current_timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Create response
        prediction_data = result.to_dict(orient='records')[0]  # Get first result
        
        # Enhanced response with detailed ML information
        response = {
            'service': 'ml_model',
            'timestamp': current_timestamp,
            'prediction': prediction_data,
            'detailed_analysis': {
                'ml_model_info': {
                    'threshold_used': autoencoder_predictor.threshold,
                    'model_status': prediction_data.get('model_status', 'active'),
                    'decision_explanation': prediction_data.get('decision_logic', 'N/A')
                },
                'reconstruction_analysis': {
                    'raw_reconstruction_error': prediction_data.get('raw_error', 0),
                    'standardized_error': prediction_data.get('standardized_error', 0),
                    'display_error': prediction_data.get('reconstruction_error', 0),
                    'max_threshold_scale': prediction_data.get('max_threshold', 1500.0)
                },
                'input_summary': {
                    'mouseMoveCount': mouse_move_count,
                    'keyPressCount': key_press_count,
                    'events_processed': len(input_data),
                    'features_extracted': features.to_dict(orient='records')[0]
                }
            },
            'metadata': {
                'ip_address': client_ip,
                'user_agent': user_agent,
                'processing_info': {
                    'features_shape': list(features.shape),
                    'scaled_features_shape': list(scaled_features.shape),
                    'model_input_ready': True
                }
            }
        }
        
        # Enhanced logging
        print(f"📋 Complete Prediction Summary:")
        print(f"   🤖 Bot Decision: {prediction_data['bot']}")
        print(f"   🔢 Raw Error: {prediction_data.get('raw_error', 'N/A')}")
        print(f"   🔢 Threshold: {autoencoder_predictor.threshold}")
        print(f"   📊 Confidence: {prediction_data['confidence']:.3f}")
        print(f"   🧠 Logic: {prediction_data.get('decision_logic', 'N/A')}")
        print(f"   📈 Display Error: {prediction_data['reconstruction_error']:.3f}")
        
        # Save enhanced prediction
        db_record = {
            'service': 'ml_model',
            'timestamp': current_timestamp,
            'prediction': prediction_data,
            'detailed_analysis': response['detailed_analysis'],
            'client_info': {
                'ip_address': client_ip,
                'user_agent': user_agent
            }
        }
        save_prediction(db_record)
        
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Error in ML predict: {e}")
        return jsonify({'error': str(e), 'service': 'ml_model'}), 500

@app.route('/predictions', methods=['GET'])
def get_predictions():
    """Get all ML predictions"""
    try:
        if PREDICTIONS_FILE.exists():
            with open(PREDICTIONS_FILE, 'r') as f:
                predictions = json.load(f)
            return jsonify({
                'service': 'ml_model',
                'total': len(predictions),
                'predictions': predictions
            }), 200
        else:
            return jsonify({
                'service': 'ml_model',
                'total': 0,
                'predictions': []
            }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'service': 'ml_model'}), 500

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get ML model information"""
    try:
        info = {
            'service': 'ml_model',
            'model_loaded': autoencoder is not None,
            'scaler_loaded': scaler is not None,
            'threshold': autoencoder_predictor.threshold if autoencoder_predictor else None,
            'model_path': str(MODELS_DIR / 'autoencoder' / 'autoencoder_model.h5'),
            'scaler_path': str(MODELS_DIR / 'autoencoder' / 'scaler.pkl'),
            'predictions_file': str(PREDICTIONS_FILE),
            'detection_logic': {
                'method': 'autoencoder_reconstruction_error',
                'threshold_value': autoencoder_predictor.threshold if autoencoder_predictor else None,
                'decision_rule': 'reconstruction_error < threshold = bot',
                'scaling_method': 'standardized_and_inverted_for_display',
                'max_threshold_scale': 1500.0
            }
        }
        
        if autoencoder:
            info['model_summary'] = {
                'input_shape': autoencoder.input_shape,
                'output_shape': autoencoder.output_shape,
                'total_params': autoencoder.count_params()
            }
        
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e), 'service': 'ml_model'}), 500

@app.route('/analyze', methods=['POST'])
def detailed_analyze():
    """Get detailed analysis without making a prediction decision - for debugging"""
    try:
        data = request.json
        print(f"🔍 Detailed analysis request received")
        
        # Extract client info
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent')
        
        # Validate required fields
        if 'mouseMoveCount' not in data or 'keyPressCount' not in data:
            return jsonify({"error": "mouseMoveCount and keyPressCount are required"}), 400
        
        mouse_move_count = data.get('mouseMoveCount')
        key_press_count = data.get('keyPressCount')
        input_data = data['events']
        
        # Convert to DataFrame
        input_df = pd.DataFrame(input_data)
        
        if autoencoder_predictor is None:
            return jsonify({"error": "ML model not available"}), 500
        
        # Extract features
        features = feature_extractor.transform(input_df)
        scaled_features = scaler.transform(features)
        
        # Get raw model output for analysis
        model_predictions = autoencoder.predict(scaled_features, verbose=0)
        reconstruction_errors = np.mean(np.square(scaled_features - model_predictions), axis=1)
        
        # Detailed analysis
        analysis = {
            'service': 'ml_model_analysis',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'input_analysis': {
                'events_count': len(input_data),
                'mouse_moves': mouse_move_count,
                'key_presses': key_press_count,
                'raw_input_sample': input_data[:5] if len(input_data) > 5 else input_data
            },
            'feature_extraction': {
                'extracted_features': features.to_dict(orient='records')[0],
                'features_shape': list(features.shape),
                'feature_names': list(features.columns)
            },
            'model_processing': {
                'scaled_features': scaled_features.tolist(),
                'model_output': model_predictions.tolist(),
                'reconstruction_errors': reconstruction_errors.tolist(),
                'threshold': autoencoder_predictor.threshold
            },
            'decision_breakdown': {
                'raw_error': float(reconstruction_errors[0]),
                'threshold_used': autoencoder_predictor.threshold,
                'is_bot': bool(reconstruction_errors[0] < autoencoder_predictor.threshold),
                'decision_margin': float(abs(reconstruction_errors[0] - autoencoder_predictor.threshold)),
                'confidence_calculation': "distance_from_threshold / threshold"
            },
            'client_info': {
                'ip_address': client_ip,
                'user_agent': user_agent
            }
        }
        
        return jsonify(analysis)
    
    except Exception as e:
        print(f"❌ Error in detailed analysis: {e}")
        import traceback
        print(f"❌ Full error traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e), 'service': 'ml_model_analysis'}), 500

if __name__ == '__main__':
    print("🚀 Starting ML Model Service...")
    print(f"📁 Models directory: {MODELS_DIR}")
    print(f"📁 Predictions file: {PREDICTIONS_FILE}")
    app.run(debug=True, host='0.0.0.0', port=5002)
