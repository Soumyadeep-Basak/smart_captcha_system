#!/usr/bin/env python3
"""
Quick health check script for all microservices
"""
import requests
import json
import time
from datetime import datetime

SERVICES = {
    'API Gateway': 'http://localhost:5000',
    'ML Model': 'http://localhost:5002', 
    'Honeypot': 'http://localhost:5001',
    'Fingerprinting': 'http://localhost:5003'
}

def check_service_health(name, url, timeout=5):
    """Check if a service is responding"""
    try:
        print(f"🔍 Checking {name} at {url}/health...")
        response = requests.get(f"{url}/health", timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {name}: HEALTHY")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Service: {data.get('service', 'unknown')}")
            return True
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectConnectError:
        print(f"🔌 {name}: CONNECTION REFUSED (service not running)")
        return False
    except requests.exceptions.Timeout:
        print(f"⏰ {name}: TIMEOUT (service may be stuck)")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"🔌 {name}: CONNECTION ERROR - {str(e)}")
        return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🏥 MICROSERVICES HEALTH CHECK")
    print("=" * 60)
    print(f"🕐 Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    healthy_count = 0
    total_count = len(SERVICES)
    
    for name, url in SERVICES.items():
        if check_service_health(name, url):
            healthy_count += 1
        print()
    
    print("=" * 60)
    print(f"📊 SUMMARY: {healthy_count}/{total_count} services healthy")
    
    if healthy_count == total_count:
        print("🎉 All services are running correctly!")
    elif healthy_count == 0:
        print("🚨 No services are responding - check if they're started")
        print("💡 Try running: scripts\\start_all_services.bat")
    else:
        print("⚠️ Some services are having issues")
    
    print("=" * 60)
    
    # If API Gateway is healthy, test the prediction endpoint
    if healthy_count > 0:
        print("\n🧪 Testing prediction endpoint...")
        try:
            test_data = {
                "mouseMoveCount": 5,
                "keyPressCount": 3,
                "events": [
                    {"timestamp": 1000, "x_position": 100, "y_position": 200, "event_name": "mousemove"},
                    {"timestamp": 1100, "x_position": 110, "y_position": 210, "event_name": "mousemove"},
                    {"timestamp": 1200, "x_position": 120, "y_position": 220, "event_name": "mousemove"},
                    {"timestamp": 1300, "x_position": 130, "y_position": 230, "event_name": "mousemove"},
                    {"timestamp": 1400, "x_position": 140, "y_position": 240, "event_name": "mousemove"}
                ]
            }
            
            response = requests.post(
                "http://localhost:5000/predict", 
                json=test_data, 
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Prediction endpoint working!")
                result = response.json()
                if 'prediction' in result and len(result['prediction']) > 0:
                    pred = result['prediction'][0]
                    print(f"   Bot detected: {pred.get('bot', 'unknown')}")
                    print(f"   Confidence: {pred.get('confidence', 'unknown')}")
                else:
                    print("⚠️ Unexpected response format")
            else:
                print(f"❌ Prediction endpoint failed: HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Prediction test failed: {e}")

if __name__ == "__main__":
    main()
