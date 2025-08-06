#!/usr/bin/env python3
"""
Test script for the enhanced bot detection system
"""

import requests
import json
from datetime import datetime

def test_enhanced_fingerprinting():
    """Test the enhanced fingerprinting with sample data"""
    
    # Sample browser fingerprint data that would come from frontend
    test_data = {
        "browserFingerprint": {
            "webdriver_detected": False,
            "plugins_count": 3,
            "mime_types_count": 4,
            "screen_width": 1920,
            "screen_height": 1080,
            "max_touch_points": 0,
            "canvas_supported": True,
            "webgl_supported": True,
            "webgl_vendor": "Google Inc. (Intel)",
            "webgl_renderer": "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "fonts_detected": 47,
            "timezone": "America/New_York",
            "language": "en-US",
            "platform": "Win32",
            "automation_signatures": [],
            "suspicious_ua_patterns": [],
            "canvas_signature": "canvas_abc123def456",
            "webgl_signature": "webgl_xyz789"
        },
        "fingerprintRisk": {
            "risk_score": 0.2,
            "risk_level": "low",
            "suspicious_features": []
        },
        "events": [
            {
                "event_name": "mousemove",
                "x_position": 100,
                "y_position": 200,
                "timestamp": int(datetime.now().timestamp() * 1000)
            }
        ],
        "mouseMoveCount": 150,
        "keyPressCount": 25,
        "metadata": {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "screen_resolution": "1920x1080",
            "timezone": "America/New_York"
        }
    }
    
    print("🧪 Testing Enhanced Bot Detection System")
    print("=" * 50)
    
    # Test the API gateway
    api_url = "http://127.0.0.1:5000/predict"
    
    try:
        print(f"📡 Sending request to {api_url}")
        response = requests.post(api_url, json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Gateway Response:")
            print(f"   Bot Prediction: {result.get('prediction', [{}])[0].get('bot', 'Unknown')}")
            print(f"   Risk Score: {result.get('risk_score', 'Unknown')}")
            print(f"   Confidence: {result.get('prediction', [{}])[0].get('confidence', 'Unknown')}")
            
            # Check enhanced features
            if 'analysisPatterns' in result:
                patterns = result['analysisPatterns']
                print("🔍 Analysis Patterns:")
                print(f"   Automation Detected: {patterns.get('automationDetected', False)}")
                print(f"   Zero Features: {patterns.get('zeroFeaturesDetected', False)}")
                print(f"   Canvas Duplicate: {patterns.get('canvasDuplicate', False)}")
            
            if 'browserFeatures' in result:
                features = result['browserFeatures']
                print("🌐 Browser Features:")
                print(f"   WebDriver: {features.get('webdriver', 'Unknown')}")
                print(f"   Plugins: {features.get('plugins', 'Unknown')}")
                print(f"   MIME Types: {features.get('mimeTypes', 'Unknown')}")
                print(f"   Fonts: {features.get('fonts', 'Unknown')}")
            
            print(f"\n📊 Full Response Preview:")
            print(json.dumps(result, indent=2)[:500] + "..." if len(json.dumps(result)) > 500 else json.dumps(result, indent=2))
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend services are running")
        print("   Run: python backend/api_gateway/app.py")
        print("   Run: python backend/services/fingerprinting/service.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_bot_data():
    """Test with bot-like data"""
    
    bot_data = {
        "browserFingerprint": {
            "webdriver_detected": True,
            "plugins_count": 0,  # Zero features - headless indicator
            "mime_types_count": 0,  # Zero features - headless indicator
            "screen_width": 1024,
            "screen_height": 768,
            "max_touch_points": 0,
            "canvas_supported": False,
            "webgl_supported": False,
            "fonts_detected": 0,  # Zero features - headless indicator
            "automation_signatures": ["webdriver", "automation"],
            "suspicious_ua_patterns": ["headless", "selenium"],
            "canvas_signature": "canvas_duplicate_hash_123",
            "webgl_signature": ""
        },
        "fingerprintRisk": {
            "risk_score": 0.9,
            "risk_level": "high",
            "suspicious_features": ["zero_plugins", "zero_mime_types", "webdriver_detected"]
        },
        "events": [
            {
                "event_name": "click",
                "x_position": 100,
                "y_position": 100,
                "timestamp": int(datetime.now().timestamp() * 1000)
            }
        ],
        "mouseMoveCount": 5,  # Very low mouse activity
        "keyPressCount": 0,
        "metadata": {
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.0.0 Safari/537.36",
            "screen_resolution": "1024x768",
            "timezone": "UTC"
        }
    }
    
    print("\n🤖 Testing with Bot-like Data")
    print("=" * 50)
    
    api_url = "http://127.0.0.1:5000/predict"
    
    try:
        response = requests.post(api_url, json=bot_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Bot Test Response:")
            print(f"   Bot Prediction: {result.get('prediction', [{}])[0].get('bot', 'Unknown')}")
            print(f"   Risk Score: {result.get('risk_score', 'Unknown')}")
            
            if 'analysisPatterns' in result:
                patterns = result['analysisPatterns']
                print("🚨 Bot Detection Patterns:")
                print(f"   Automation Detected: {patterns.get('automationDetected', False)}")
                print(f"   Zero Features: {patterns.get('zeroFeaturesDetected', False)}")
                print(f"   Zero Feature List: {patterns.get('zeroFeaturesList', [])}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔬 Enhanced Bot Detection System Test")
    print("=====================================\n")
    
    # Test with human-like data
    test_enhanced_fingerprinting()
    
    # Test with bot-like data
    test_bot_data()
    
    print("\n✨ Test completed!")
    print("\n📌 To test admin interface:")
    print("   1. Start the frontend: cd frontend && npm run dev")
    print("   2. Visit: http://localhost:3000/admin")
    print("   3. Click on recent entries to see enhanced analysis")
