import sys
import os
sys.path.append('d:/hack/botv1/bots')

print("🔍 Testing ML Model Loading...")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow version: {tf.__version__}")
except Exception as e:
    print(f"❌ TensorFlow import error: {e}")

try:
    import joblib
    print("✅ Joblib imported successfully")
except Exception as e:
    print(f"❌ Joblib import error: {e}")

try:
    import pandas as pd
    print("✅ Pandas imported successfully")
except Exception as e:
    print(f"❌ Pandas import error: {e}")

try:
    import numpy as np
    print("✅ Numpy imported successfully")
except Exception as e:
    print(f"❌ Numpy import error: {e}")

# Test model loading
os.chdir('d:/hack/botv1/bots')
print(f"📁 Current directory: {os.getcwd()}")

try:
    from tensorflow.keras.models import load_model
    from keras.losses import MeanSquaredError
    print("✅ Keras imports successful")
    
    print("🤖 Loading autoencoder model...")
    autoencoder = load_model('autoencoder_model.h5', custom_objects={'mse': MeanSquaredError()})
    print(f"✅ Autoencoder loaded! Input shape: {autoencoder.input_shape}")
    print(f"✅ Autoencoder loaded! Output shape: {autoencoder.output_shape}")
    
except Exception as e:
    print(f"❌ Model loading error: {e}")

try:
    print("📊 Loading scaler...")
    scaler = joblib.load('scaler.pkl')
    print(f"✅ Scaler loaded! Type: {type(scaler)}")
    
except Exception as e:
    print(f"❌ Scaler loading error: {e}")

print("\n🧪 Testing with sample data...")
try:
    # Test with sample data
    sample_data = np.random.random((1, 8))  # Assuming 8 features
    print(f"📥 Sample input shape: {sample_data.shape}")
    
    if 'scaler' in locals():
        scaled_data = scaler.transform(sample_data)
        print(f"📊 Scaled data shape: {scaled_data.shape}")
        
        if 'autoencoder' in locals():
            prediction = autoencoder.predict(scaled_data)
            print(f"🔮 Prediction shape: {prediction.shape}")
            
            # Calculate reconstruction error
            reconstruction_error = np.mean(np.square(scaled_data - prediction))
            print(f"📈 Reconstruction error: {reconstruction_error}")
            
            if reconstruction_error > 0.5:
                print("🤖 Would be classified as: BOT")
            else:
                print("👤 Would be classified as: HUMAN")
        else:
            print("❌ Cannot test prediction - model not loaded")
    else:
        print("❌ Cannot test scaling - scaler not loaded")
        
except Exception as e:
    print(f"❌ Testing error: {e}")

print("\n✅ Model testing complete!")
