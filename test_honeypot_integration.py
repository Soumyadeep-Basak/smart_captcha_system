"""
Test script to verify the complete honeypot integration
Tests the Flask API endpoint with honeypot data
"""

import requests
import json
from datetime import datetime

def test_honeypot_integration():
    """Test the complete honeypot system integration"""
    
    print("🧪 Testing Complete Honeypot Integration")
    print("=" * 50)
    
    # API endpoint
    api_url = "http://localhost:5000/api/predict"
    
    # Test 1: Clean user submission (no honeypots triggered)
    print("\n📝 Test 1: Clean User Submission")
    clean_data = {
        "events": [
            {"event_name": "click", "timestamp": 1000, "x_position": 100, "y_position": 200},
            {"event_name": "mousemove", "timestamp": 1500, "x_position": 150, "y_position": 250},
            {"event_name": "click", "timestamp": 2000, "x_position": 200, "y_position": 300}
        ],
        "honeypot_data": {
            "hidden_honeypot_field": "",  # Empty - good user
            "fake_submit_clicked": False,  # Not clicked - good user
            "js_optional_field": "",      # Empty - good user
            "js_enabled": True,           # JS working - good user
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        "form_data": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890"
        }
    }
    
    # Test 2: Bot submission with all honeypots triggered
    print("\n📝 Test 2: Bot with All Honeypots Triggered")
    bot_data = {
        "events": [],  # No events - typical bot behavior
        "honeypot_data": {
            "hidden_honeypot_field": "https://malicious-site.com",  # Bot filled hidden field
            "fake_submit_clicked": True,                            # Bot clicked fake submit
            "js_optional_field": "bot filled this field",         # Bot filled JS field
            "js_enabled": False,                                   # No JS - bot behavior
            "user_agent": "Python-urllib/3.9"                     # Bot user agent
        },
        "form_data": {
            "name": "Bot User",
            "email": "bot@spam.com",
            "phone": "0000000000"
        }
    }
    
    # Test 3: Suspicious user with one honeypot triggered
    print("\n📝 Test 3: Suspicious User - Hidden Field Filled")
    suspicious_data = {
        "events": [
            {"event_name": "click", "timestamp": 500, "x_position": 50, "y_position": 100},
            {"event_name": "click", "timestamp": 600, "x_position": 200, "y_position": 300}
        ],
        "honeypot_data": {
            "hidden_honeypot_field": "www.example.com",  # Filled hidden field - suspicious
            "fake_submit_clicked": False,
            "js_optional_field": "",
            "js_enabled": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        "form_data": {
            "name": "Suspicious User",
            "email": "suspect@example.com",
            "phone": "5555555555"
        }
    }
    
    test_cases = [
        ("Clean User", clean_data),
        ("Bot (All Honeypots)", bot_data),
        ("Suspicious User", suspicious_data)
    ]
    
    for test_name, data in test_cases:
        print(f"\n🎯 Testing: {test_name}")
        print("-" * 30)
        
        try:
            response = requests.post(api_url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Status: {response.status_code}")
                print(f"🤖 Bot Detected: {result.get('is_bot', 'Unknown')}")
                print(f"🍯 Honeypot Score: {result.get('honeypot_score', 'N/A'):.3f}")
                print(f"📊 Total Score: {result.get('total_score', 'N/A'):.3f}")
                print(f"⚠️ Threat Level: {result.get('threat_level', 'Unknown')}")
                
                # Honeypot specific details
                if 'honeypot_results' in result:
                    honeypot_results = result['honeypot_results']
                    print(f"🎯 Honeypots Triggered: {honeypot_results.get('honeypots_triggered', 0)}/3")
                    
                    # Show which honeypots were triggered
                    if 'detailed_results' in honeypot_results:
                        for honeypot_type, details in honeypot_results['detailed_results'].items():
                            if details.get('triggered', False):
                                print(f"   🚨 {honeypot_type}: {details.get('details', 'Triggered')}")
                
                print(f"💡 Recommendation: {result.get('recommendation', 'Unknown')}")
                
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Flask API not running on localhost:5000")
            print("   Please start the Flask server first with: python app.py")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Honeypot Integration Test Complete")

if __name__ == "__main__":
    test_honeypot_integration()
