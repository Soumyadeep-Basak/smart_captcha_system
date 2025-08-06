#!/usr/bin/env python3
"""
Quick test script to check the admin API endpoint
"""

import requests
import json
import sys

def test_predictions_endpoint():
    """Test the /predictions endpoint"""
    try:
        print("🔍 Testing predictions endpoint...")
        url = "http://127.0.0.1:5000/predictions"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Got {len(data) if isinstance(data, list) else 'unknown'} predictions")
            
            if isinstance(data, list) and len(data) > 0:
                print(f"📊 Sample prediction structure:")
                sample = data[0]
                print(f"   Keys: {list(sample.keys())}")
                if 'ipAddress' in sample:
                    print(f"   IP: {sample.get('ipAddress')}")
                if 'isBot' in sample:
                    print(f"   IsBot: {sample.get('isBot')}")
                if 'timestamp' in sample:
                    print(f"   Timestamp: {sample.get('timestamp')}")
            
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running on http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_endpoint():
    """Test the /health endpoint"""
    try:
        print("🔍 Testing health endpoint...")
        url = "http://127.0.0.1:5000/health"
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: API server not running")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Admin API Endpoints\n")
    
    # Test health first
    health_ok = test_health_endpoint()
    print()
    
    if health_ok:
        # Test predictions
        predictions_ok = test_predictions_endpoint()
        print()
        
        if predictions_ok:
            print("✅ All tests passed! Admin page should work.")
        else:
            print("❌ Predictions endpoint failed.")
    else:
        print("❌ API server is not responding. Please start it first:")
        print("   cd backend/api && python app.py")
    
    print("\nDone!")
