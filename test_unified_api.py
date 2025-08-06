#!/usr/bin/env python3
"""
Test script for the Unified Bot Detection API
"""
import requests
import json
import time
from datetime import datetime

API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Architecture: {data.get('architecture', 'unknown')}")
            print(f"   Modules: {list(data.get('modules', {}).keys())}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_prediction():
    """Test main prediction endpoint with sample data"""
    print("\n🧠 Testing Prediction Endpoint...")
    
    test_data = {
        "mouseMoveCount": 8,
        "keyPressCount": 5,
        "events": [
            {"timestamp": 1000, "x_position": 100, "y_position": 150, "event_name": "mousemove"},
            {"timestamp": 1050, "x_position": 105, "y_position": 155, "event_name": "mousemove"},
            {"timestamp": 1100, "x_position": 110, "y_position": 160, "event_name": "mousemove"},
            {"timestamp": 1150, "x_position": 115, "y_position": 165, "event_name": "mousemove"},
            {"timestamp": 1200, "x_position": 120, "y_position": 170, "event_name": "mousemove"},
            {"timestamp": 1250, "x_position": 125, "y_position": 175, "event_name": "mousemove"},
            {"timestamp": 1300, "x_position": 130, "y_position": 180, "event_name": "mousemove"},
            {"timestamp": 1350, "x_position": 135, "y_position": 185, "event_name": "mousemove"}
        ]
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict", 
            json=test_data, 
            timeout=15,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Prediction successful!")
            
            # Check frontend compatibility
            required_fields = ['ip_address', 'user_agent', 'current_timestamp', 'prediction']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print(f"⚠️ Missing frontend fields: {missing_fields}")
            else:
                print("✅ Frontend compatibility: All required fields present")
            
            # Check prediction format
            if 'prediction' in result and len(result['prediction']) > 0:
                pred = result['prediction'][0]
                print(f"   🤖 Bot detected: {pred.get('bot', 'unknown')}")
                print(f"   📊 Confidence: {pred.get('confidence', 'unknown')}")
                print(f"   🔢 Reconstruction error: {pred.get('reconstruction_error', 'unknown')}")
                print(f"   🔢 Raw error: {pred.get('raw_error', 'unknown')}")
                
                # Check enhanced analysis
                if 'enhanced_analysis' in result:
                    enhanced = result['enhanced_analysis']
                    print(f"   🧠 ML Method: {enhanced['ml_analysis'].get('method', 'unknown')}")
                    print(f"   🍯 Threat Level: {enhanced['honeypot_analysis'].get('threat_level', 'unknown')}")
                    print(f"   👆 Risk Level: {enhanced['fingerprint_analysis'].get('risk_level', 'unknown')}")
                
                return True
            else:
                print("❌ Invalid prediction format")
                return False
        else:
            print(f"❌ Prediction failed: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction test error: {e}")
        return False

def test_detailed_analysis():
    """Test detailed analysis endpoint"""
    print("\n🔍 Testing Detailed Analysis Endpoint...")
    
    test_data = {
        "events": [
            {"timestamp": 1000, "x_position": 200, "y_position": 200, "event_name": "mousemove"},
            {"timestamp": 1010, "x_position": 200, "y_position": 200, "event_name": "mousemove"},  # No movement
            {"timestamp": 1020, "x_position": 200, "y_position": 200, "event_name": "mousemove"},
            {"timestamp": 1030, "x_position": 200, "y_position": 200, "event_name": "mousemove"},
            {"timestamp": 1040, "x_position": 200, "y_position": 200, "event_name": "mousemove"}
        ]
    }
    
    try:
        response = requests.post(
            f"{API_URL}/analyze/detailed", 
            json=test_data, 
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Detailed analysis successful!")
            
            if 'module_results' in result:
                modules = result['module_results']
                print(f"   🧠 ML Result: {modules.get('ml_model', {}).get('bot', 'unknown')}")
                print(f"   🍯 Honeypot Result: {modules.get('honeypot', {}).get('honeypot_verdict', {}).get('is_bot', 'unknown')}")
                print(f"   👆 Fingerprint Result: {modules.get('fingerprinting', {}).get('verdict', {}).get('is_suspicious', 'unknown')}")
            
            return True
        else:
            print(f"❌ Detailed analysis failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Detailed analysis error: {e}")
        return False

def test_modules_info():
    """Test modules info endpoint"""
    print("\n🧩 Testing Modules Info Endpoint...")
    
    try:
        response = requests.get(f"{API_URL}/modules/info", timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Modules info retrieved!")
            
            if 'modules' in result:
                for module_name, module_info in result['modules'].items():
                    print(f"   📦 {module_name}: {module_info.get('module', 'unknown')}")
            
            return True
        else:
            print(f"❌ Modules info failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Modules info error: {e}")
        return False

def main():
    print("="*60)
    print("🧪 UNIFIED BOT DETECTION API - TEST SUITE")
    print("="*60)
    print(f"🕐 Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Health Check", test_health),
        ("Prediction Endpoint", test_prediction),
        ("Detailed Analysis", test_detailed_analysis),
        ("Modules Info", test_modules_info)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "="*60)
    print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The unified API is working correctly.")
        print("💡 Your frontend should now be able to connect without issues.")
    elif passed == 0:
        print("🚨 All tests failed - API may not be running")
        print("💡 Try running: scripts\\start_unified_api.bat")
    else:
        print("⚠️ Some tests failed - API is partially working")
    
    print("="*60)

if __name__ == "__main__":
    main()
