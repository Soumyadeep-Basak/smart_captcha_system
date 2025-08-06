#!/usr/bin/env python3
"""
Test script for the new microservices backend
"""

import requests
import json
import time
from datetime import datetime

# Test data - sample mouse events
test_data = {
    "mouseMoveCount": 15,
    "keyPressCount": 8,
    "events": [
        {"timestamp": 1000, "x_position": 100, "y_position": 200, "event_name": "mousemove"},
        {"timestamp": 1100, "x_position": 110, "y_position": 210, "event_name": "mousemove"},
        {"timestamp": 1200, "x_position": 120, "y_position": 220, "event_name": "mousemove"},
        {"timestamp": 1300, "x_position": 130, "y_position": 230, "event_name": "mousemove"},
        {"timestamp": 1400, "x_position": 140, "y_position": 240, "event_name": "mousemove"},
        {"timestamp": 1500, "x_position": 150, "y_position": 250, "event_name": "mousemove"},
        {"timestamp": 1600, "x_position": 160, "y_position": 260, "event_name": "mousemove"},
        {"timestamp": 1700, "x_position": 170, "y_position": 270, "event_name": "mousemove"},
    ]
}

def test_service_health(service_name, url):
    """Test if a service is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name}: HEALTHY")
            return True
        else:
            print(f"❌ {service_name}: UNHEALTHY (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {service_name}: OFFLINE ({e})")
        return False

def test_ml_prediction(base_url):
    """Test ML prediction endpoint"""
    try:
        print(f"\n🧠 Testing ML Prediction at {base_url}")
        response = requests.post(f"{base_url}/predict", json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ML Prediction successful!")
            print(f"   Bot detected: {result.get('prediction', {}).get('bot', 'Unknown')}")
            print(f"   Confidence: {result.get('prediction', {}).get('confidence', 'Unknown')}")
            print(f"   Reconstruction error: {result.get('prediction', {}).get('reconstruction_error', 'Unknown')}")
            return True
        else:
            print(f"❌ ML Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ML Prediction error: {e}")
        return False

def test_gateway_prediction():
    """Test prediction through API Gateway"""
    try:
        print(f"\n🚪 Testing API Gateway Prediction")
        response = requests.post("http://localhost:5000/predict", json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Gateway prediction successful!")
            print(f"   Gateway timestamp: {result.get('gateway', {}).get('gateway_timestamp', 'Unknown')}")
            print(f"   ML Service response: {result.get('ml_service', {}).get('service', 'Unknown')}")
            print(f"   Final prediction: {result.get('prediction', {})}")
            return True
        else:
            print(f"❌ Gateway prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Gateway prediction error: {e}")
        return False

def main():
    """Main testing function"""
    print("🧪 BACKEND MICROSERVICES TEST")
    print("=" * 50)
    
    # Service endpoints
    services = {
        "API Gateway": "http://localhost:5000",
        "ML Model Service": "http://localhost:5002", 
        "Honeypot Service": "http://localhost:5001",
        "Fingerprinting Service": "http://localhost:5003"
    }
    
    print("\n1️⃣ TESTING SERVICE HEALTH")
    print("-" * 30)
    healthy_services = []
    
    for name, url in services.items():
        if test_service_health(name, url):
            healthy_services.append((name, url))
    
    print(f"\n📊 Health Summary: {len(healthy_services)}/{len(services)} services online")
    
    # Test ML Model directly if available
    ml_service_url = "http://localhost:5002"
    if ("ML Model Service", ml_service_url) in healthy_services:
        print("\n2️⃣ TESTING ML MODEL SERVICE")
        print("-" * 30)
        test_ml_prediction(ml_service_url)
    
    # Test API Gateway if available
    gateway_url = "http://localhost:5000"
    if ("API Gateway", gateway_url) in healthy_services:
        print("\n3️⃣ TESTING API GATEWAY")
        print("-" * 30)
        test_gateway_prediction()
    
    print("\n✨ TESTING COMPLETE!")
    print("=" * 50)
    
    if len(healthy_services) == 0:
        print("⚠️  No services are running. Please start services using:")
        print("   scripts\\start_all_services.bat")
    elif len(healthy_services) < len(services):
        print("⚠️  Some services are offline. Check service logs.")
    else:
        print("🎉 All services are operational!")

if __name__ == "__main__":
    main()
