# ML Model Module - Lightweight Bot Detection
import pandas as pd
import numpy as np
import random
from datetime import datetime
import json
import os
from pathlib import Path

class MLModelModule:
    def __init__(self):
        self.threshold = 500
        self.model_loaded = False
        self.scaler_loaded = False
        print("🧠 Initializing ML Model Module (Lightweight Mode)")
        
        # Try to load TensorFlow model, but fallback if issues
        try:
            self._load_tensorflow_model()
        except Exception as e:
            print(f"⚠️ TensorFlow loading failed: {e}")
            print("🔄 Switching to heuristic-based detection")
            self.model_loaded = False
    
    def _load_tensorflow_model(self):
        """Attempt to load TensorFlow model with timeout protection"""
        try:
            # Set environment variables to suppress TensorFlow warnings
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            
            import tensorflow as tf
            tf.get_logger().setLevel('ERROR')
            
            from tensorflow.keras.models import load_model
            from tensorflow.keras.losses import MeanSquaredError
            import joblib
            
            BASE_DIR = Path(__file__).parent.parent.parent
            model_path = BASE_DIR / 'models' / 'autoencoder' / 'autoencoder_model.h5'
            scaler_path = BASE_DIR / 'models' / 'autoencoder' / 'scaler.pkl'
            
            if model_path.exists() and scaler_path.exists():
                self.autoencoder = load_model(str(model_path), custom_objects={'mse': MeanSquaredError()})
                self.scaler = joblib.load(str(scaler_path))
                self.model_loaded = True
                self.scaler_loaded = True
                print("✅ TensorFlow model loaded successfully!")
            else:
                print("❌ Model files not found, using fallback")
                
        except Exception as e:
            print(f"❌ TensorFlow model loading error: {e}")
            self.model_loaded = False
    
    def extract_features(self, events):
        """Extract features from mouse movement events"""
        if not events or len(events) < 2:
            return pd.DataFrame([{
                'speed_mean': 0, 'speed_std': 0,
                'acceleration_mean': 0, 'acceleration_std': 0,
                'angle_diff_mean': 0, 'angle_diff_std': 0
            }])
        
        df = pd.DataFrame(events)
        
        # Handle missing positions
        df.loc[(df['x_position'] == 0) & (df['y_position'] == 0), ['x_position', 'y_position']] = np.nan
        df[['x_position', 'y_position']] = df[['x_position', 'y_position']].ffill()
        
        # Calculate movement metrics
        df['time_diff'] = df['timestamp'].diff().fillna(0)
        df['distance'] = np.sqrt((df['x_position'].diff())**2 + (df['y_position'].diff())**2).fillna(0)
        df['speed'] = df['distance'] / df['time_diff'].replace(0, np.nan)
        df['acceleration'] = df['speed'].diff() / df['time_diff'].replace(0, np.nan)
        df.fillna(0, inplace=True)
        
        # Calculate angle differences
        def compute_angle_diff(x1, y1, x2, y2):
            angle = np.arctan2(y2 - y1, x2 - x1)
            return np.degrees(angle)
        
        df['angle_diff'] = compute_angle_diff(
            df['x_position'].shift(1), df['y_position'].shift(1),
            df['x_position'], df['y_position']
        ).fillna(0)
        
        # Create feature summary
        features = pd.DataFrame({
            'speed_mean': [df['speed'].mean()],
            'speed_std': [df['speed'].std()],
            'acceleration_mean': [df['acceleration'].mean()],
            'acceleration_std': [df['acceleration'].std()],
            'angle_diff_mean': [df['angle_diff'].mean()],
            'angle_diff_std': [df['angle_diff'].std()]
        })
        
        return features
    
    def predict_with_tensorflow(self, features):
        """Use TensorFlow model for prediction - EXACT LOGIC FROM script2_no_mongo.py"""
        try:
            print(f"🧠 Running ML prediction on {features.shape} features...")
            
            scaled_features = self.scaler.transform(features)
            print(f"🔧 Scaled features shape: {scaled_features.shape}")
            
            # Get predictions from the autoencoder
            predictions = self.autoencoder.predict(scaled_features, verbose=0)
            print(f"🔧 Autoencoder output shape: {predictions.shape}")
            
            # Calculate reconstruction error - EXACT SAME LOGIC
            reconstruction_errors = np.mean(np.square(scaled_features - predictions), axis=1)
            raw_error = float(reconstruction_errors[0])
            
            # PROCESSING FOR DISPLAY: Standardize and invert reconstruction errors
            # Step 1: Standardize to 0-1 range using 1500 as max threshold
            max_threshold = 1500.0
            standardized_errors = np.clip(reconstruction_errors / max_threshold, 0, 1)
            
            # Step 2: Invert the values (1 - standardized_value)
            display_errors = 1.0 - standardized_errors
            display_error = float(display_errors[0])
            
            print(f"🔢 Raw reconstruction error: {raw_error}")
            print(f"🔢 Processed display errors: {display_errors}")
            
            # Determine if it's a bot based on reconstruction error (INVERTED LOGIC)
            # Model was trained opposite way: error < 300 = bot, error >= 300 = human
            is_bot = reconstruction_errors < self.threshold
            bot_result = bool(is_bot[0])
            
            # CONVERT THRESHOLD TO DISPLAY FORMAT for consistent output
            threshold_standardized = np.clip(self.threshold / max_threshold, 0, 1)
            threshold_display = 1.0 - threshold_standardized
            
            print(f"🔢 Bot detection threshold: {self.threshold} (raw) -> {threshold_display:.4f} (display)")
            print(f"🔢 Bot detection results: {is_bot}")
            print(f"🤖 Bot detection logic: {raw_error} < {self.threshold} = {bot_result}")
            
            # Calculate confidence based on distance from threshold in DISPLAY format
            distance_from_threshold_display = abs(display_error - threshold_display)
            confidence = min(distance_from_threshold_display / threshold_display if threshold_display > 0 else 1.0, 1.0)
            
            result = {
                'bot': bot_result,
                'reconstruction_error': display_error,  # Use processed display error like original
                'confidence': float(confidence),
                'raw_error': display_error,  # SHOW DISPLAY FORMAT as raw_error for frontend
                'threshold_used': threshold_display,  # SHOW DISPLAY FORMAT threshold
                'decision_logic': f"display_error ({display_error:.4f}) vs threshold ({threshold_display:.4f}) | raw_logic: {raw_error:.2f} < {self.threshold} = {bot_result}",
                'model_status': 'tensorflow_active',
                'method': 'autoencoder_reconstruction',
                'processing_details': {
                    'max_threshold': max_threshold,
                    'raw_reconstruction_error': raw_error,
                    'standardized_error': float(standardized_errors[0]),
                    'display_error_inverted': display_error,
                    'threshold_raw': self.threshold,
                    'threshold_display': threshold_display,
                    'original_logic': 'script2_no_mongo.py'
                }
            }
            
            print(f"✅ ML prediction complete: Bot={bot_result}, Display_Error={display_error:.4f}, Threshold_Display={threshold_display:.4f}")
            return result
            
        except Exception as e:
            print(f"❌ TensorFlow prediction error: {e}")
            return self.predict_with_heuristics(features)
    
    def predict_with_heuristics(self, features):
        """Fallback heuristic-based prediction - Using same display format as TensorFlow"""
        try:
            feature_dict = features.iloc[0].to_dict()
            
            # Heuristic bot detection - STRICTER LOGIC
            bot_score = 0.3  # Start with higher base score for basic patterns
            reasons = []
            
            # Check for suspicious patterns
            speed_mean = feature_dict.get('speed_mean', 0)
            speed_std = feature_dict.get('speed_std', 0)
            accel_mean = abs(feature_dict.get('acceleration_mean', 0))
            angle_std = feature_dict.get('angle_diff_std', 0)
            
            print(f"🔍 Heuristic Analysis:")
            print(f"   Speed Mean: {speed_mean:.3f}")
            print(f"   Speed Std: {speed_std:.3f}")
            print(f"   Acceleration Mean: {accel_mean:.3f}")
            print(f"   Angle Std: {angle_std:.3f}")
            
            # Bot indicators - MORE AGGRESSIVE DETECTION
            if speed_mean > 3.0:  # Lowered threshold from 5.0
                bot_score += 0.3
                reasons.append("high_speed")
            
            if speed_std < 1.0:  # Very consistent speed (raised from 0.5)
                bot_score += 0.3
                reasons.append("consistent_speed")
            
            if accel_mean > 5.0:  # High acceleration (lowered from 10.0)
                bot_score += 0.3
                reasons.append("high_acceleration")
            
            if angle_std < 10.0:  # Very straight movement (raised from 5.0)
                bot_score += 0.3
                reasons.append("straight_movement")
            
            # Additional checks for basic/bot patterns
            if speed_mean == 0 and accel_mean == 0:  # No movement at all
                bot_score += 0.5
                reasons.append("no_movement")
            
            if speed_std == 0:  # Perfect consistency (clearly bot)
                bot_score += 0.4
                reasons.append("perfect_consistency")
            
            # Reduce randomness and bias toward bot detection
            bot_score += random.uniform(-0.05, 0.1)  # Slight bias toward bot
            bot_score = max(0.2, min(1, bot_score))  # Minimum score of 0.2
            
            print(f"🔍 Bot Score: {bot_score:.3f}, Reasons: {reasons}")
            
            # Convert to reconstruction error format (inverted logic like original)
            # Higher bot_score = lower raw_error = more likely bot
            raw_error = 300 + (0.5 - bot_score) * 400  # Inverted: high bot_score = low error
            is_bot = raw_error < self.threshold
            
            # APPLY SAME DISPLAY CONVERSION AS TENSORFLOW VERSION
            # Step 1: Standardize to 0-1 range using 1500 as max threshold
            max_threshold = 1500.0
            standardized_error = np.clip(raw_error / max_threshold, 0, 1)
            
            # Step 2: Invert the values (1 - standardized_value)
            display_error = 1.0 - standardized_error
            
            # Convert threshold to display format too
            threshold_standardized = np.clip(self.threshold / max_threshold, 0, 1)
            threshold_display = 1.0 - threshold_standardized
            
            # Confidence based on distance from threshold in display format
            distance_from_threshold_display = abs(display_error - threshold_display)
            confidence = min(distance_from_threshold_display / threshold_display if threshold_display > 0 else 1.0, 1.0)
            
            result = {
                'bot': is_bot,
                'reconstruction_error': float(display_error),  # DISPLAY FORMAT
                'confidence': float(confidence),
                'raw_error': float(display_error),  # SHOW DISPLAY FORMAT as raw_error for frontend
                'threshold_used': float(threshold_display),  # SHOW DISPLAY FORMAT threshold
                'decision_logic': f"display_error ({display_error:.4f}) vs threshold ({threshold_display:.4f}) | heuristic_score ({bot_score:.2f}) -> raw_logic: {raw_error:.1f} < {self.threshold} = {is_bot}",
                'model_status': 'heuristic_fallback',
                'method': 'heuristic_analysis',
                'bot_indicators': reasons,
                'heuristic_details': {
                    'speed_mean': speed_mean,
                    'speed_std': speed_std,
                    'acceleration_mean': accel_mean,
                    'angle_std': angle_std,
                    'bot_score': bot_score,
                    'logic': 'aggressive_bot_detection'
                },
                'processing_details': {
                    'max_threshold': max_threshold,
                    'raw_reconstruction_error': raw_error,
                    'standardized_error': float(standardized_error),
                    'display_error_inverted': display_error,
                    'threshold_raw': self.threshold,
                    'threshold_display': threshold_display
                }
            }
            
            print(f"✅ Heuristic prediction: Bot={is_bot}, Display_Error={display_error:.4f}, Threshold_Display={threshold_display:.4f}")
            return result
            
        except Exception as e:
            print(f"❌ Heuristic prediction error: {e}")
            # Convert error fallback to display format too
            error_raw = 100.0  # Low error = bot
            error_standardized = np.clip(error_raw / 1500.0, 0, 1)
            error_display = 1.0 - error_standardized
            
            threshold_standardized = np.clip(self.threshold / 1500.0, 0, 1)
            threshold_display = 1.0 - threshold_standardized
            
            return {
                'bot': True,  # Default to bot on error
                'reconstruction_error': float(error_display),
                'confidence': 0.7,
                'raw_error': float(error_display),  # DISPLAY FORMAT
                'threshold_used': float(threshold_display),  # DISPLAY FORMAT
                'decision_logic': f'error_fallback = bot (display_format)',
                'model_status': 'error',
                'method': 'error_fallback'
            }
    
    def predict(self, events):
        """Main prediction method"""
        try:
            print(f"🧠 ML Module: Processing {len(events)} events")
            
            # Extract features
            features = self.extract_features(events)
            
            # Choose prediction method
            if self.model_loaded and self.scaler_loaded:
                result = self.predict_with_tensorflow(features)
            else:
                result = self.predict_with_heuristics(features)
            
            print(f"🎯 ML Prediction: Bot={result['bot']}, Confidence={result['confidence']:.3f}, Method={result.get('method', 'unknown')}")
            
            return result
            
        except Exception as e:
            print(f"❌ ML Module prediction error: {e}")
            return {
                'bot': True,
                'reconstruction_error': 0.95,
                'confidence': 0.8,
                'raw_error': 500.0,
                'threshold_used': self.threshold,
                'decision_logic': f'module_error: {str(e)}',
                'model_status': 'error',
                'method': 'error_fallback'
            }
    
    def get_info(self):
        """Get module information"""
        return {
            'module': 'ml_model',
            'model_loaded': self.model_loaded,
            'scaler_loaded': self.scaler_loaded,
            'threshold': self.threshold,
            'methods_available': ['tensorflow', 'heuristic', 'fallback'],
            'current_method': 'tensorflow' if self.model_loaded else 'heuristic'
        }
