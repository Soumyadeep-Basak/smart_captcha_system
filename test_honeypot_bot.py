#!/usr/bin/env python3
"""
Test Bot to Trigger 8-Layer Honeypot System
This bot will intentionally trigger multiple honeypots to test the detection system.
"""

import requests
import json
import time
import random

def test_honeypot_triggers():
    """Test the honeypot detection by sending data that should trigger multiple traps"""
    
    # API endpoint
    url = 'http://127.0.0.1:5000/predict'
    
    # Simulate bot events (minimal mouse/keyboard activity)
    events = [
        {
            "event_name": "mousemove",
            "timestamp": "2025-01-20T10:00:00.000Z",
            "x_position": 100,
            "y_position": 100
        },
        {
            "event_name": "click",
            "timestamp": "2025-01-20T10:00:01.000Z", 
            "x_position": 200,
            "y_position": 150
        }
    ]
    
    # Test Case 1: Trigger Multiple Honeypots (Advanced Bot)
    print("🤖 Testing Advanced Bot - Triggering Multiple Honeypots")
    
    payload_advanced = {
        "mouseMoveCount": 15,  # Low mouse activity
        "keyPressCount": 8,    # Low keyboard activity
        "events": events,
        
        # Browser fingerprint that suggests automation
        "browserFingerprint": {
            "webdriver_detected": True,  # Should trigger fingerprinting
            "plugins_count": 0,
            "mime_types_count": 0,
            "screen_width": 1920,
            "screen_height": 1080,
            "max_touch_points": 0,
            "suspicious_ua_patterns": ["HeadlessChrome", "automation"]
        },
        
        # Honeypot data that triggers multiple traps
        "honeypot_data": {
            # Layer 1: Enhanced CSS Hidden Field - TRIGGERED
            "hidden_honeypot_field": "http://malicious-bot-site.com",
            "enhanced_css_hidden_triggered": True,
            
            # Layer 2: Fake Submit Button - TRIGGERED  
            "fake_submit_clicked": True,
            
            # Layer 3: JS Optional Field - TRIGGERED
            "js_optional_field": "automated_value",
            "js_optional_field_triggered": True,
            "js_enabled": False,  # Pretend JS is disabled
            
            # Layer 4: Focus Order - TRIGGERED
            "focus_trail": ["phone", "name", "aadhaar", "email"],  # Unnatural order
            "expected_focus_order": ["name", "email", "aadhaar", "eid", "fathers_name", "phone"],
            "focus_order_triggered": True,
            
            # Layer 5: Offscreen Mouse - NOT TRIGGERED
            "offscreen_mouse_triggered": False,
            
            # Layer 6: JS Delayed Field - TRIGGERED
            "js_delayed_field_triggered": True,
            
            # Layer 7: Canvas Fingerprinting - TRIGGERED
            "canvas_fingerprint_triggered": True,
            
            # Layer 8: DOM Mutation - TRIGGERED  
            "dom_mutation_triggered": True,
            "dom_stable": False,
            "page_load_duration": 0.8  # Submitted too quickly
        },
        
        "metadata": {
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 HeadlessChrome/91.0.4472.124",
            "screen_resolution": "1920x1080",
            "timezone": "UTC",
            "language": "en-US",
            "platform": "Linux x86_64",
            "webdriver_detected": True,
            "plugins_count": 0,
            "mime_types_count": 0,
            "touch_points": 0,
            "hardware_concurrency": 4,
            "device_memory": 8
        }
    }
    
    try:
        print("📤 Sending advanced bot request...")
        response = requests.post(url, json=payload_advanced, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Advanced Bot Response received!")
            
            # Check prediction
            prediction = result.get('prediction', [{}])[0]
            print(f"🤖 Bot Detected: {prediction.get('bot', 'Unknown')}")
            print(f"📊 Confidence: {prediction.get('confidence', 'Unknown')}")
            
            # Check honeypot analysis
            honeypot_analysis = result.get('enhanced_analysis', {}).get('honeypot_analysis', {})
            if honeypot_analysis:
                print(f"🍯 Honeypot Analysis:")
                print(f"   • Threat Detected: {honeypot_analysis.get('threat_detected', 'Unknown')}")
                print(f"   • Threat Level: {honeypot_analysis.get('threat_level', 'Unknown')}")
                print(f"   • Honeypot Score: {honeypot_analysis.get('honeypot_score', 0):.3f}")
                
                summary = honeypot_analysis.get('honeypot_summary', {})
                if summary:
                    triggered = summary.get('triggered_honeypots', 0)
                    total = summary.get('total_honeypots', 8)
                    print(f"   • Honeypots Triggered: {triggered}/{total}")
                    
                    triggered_types = summary.get('honeypot_types_triggered', [])
                    if triggered_types:
                        print(f"   • Triggered Types: {', '.join(triggered_types)}")
                
                # Show detailed results
                details = honeypot_analysis.get('honeypot_details', {}).get('detailed_results', {})
                if details:
                    print(f"🔍 Detailed Honeypot Results:")
                    for trap_type, data in details.items():
                        status = "🚨 TRIGGERED" if data.get('triggered', False) else "✅ CLEAN"
                        score = data.get('score', 0)
                        print(f"   • {trap_type}: {status} (Score: {score:.1f})")
            
            print("\n" + "="*60 + "\n")
            
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test Case 2: Clean Human User (should not trigger honeypots)
    print("👤 Testing Clean Human User - No Honeypots")
    
    payload_human = {
        "mouseMoveCount": 245,  # High mouse activity
        "keyPressCount": 89,    # High keyboard activity  
        "events": events + [{"event_name": "mousemove", "timestamp": f"2025-01-20T10:00:{i:02d}.000Z", "x_position": random.randint(50, 800), "y_position": random.randint(50, 600)} for i in range(20)],
        
        # Normal browser fingerprint
        "browserFingerprint": {
            "webdriver_detected": False,
            "plugins_count": 23,
            "mime_types_count": 67,
            "screen_width": 1920,
            "screen_height": 1080,
            "max_touch_points": 10,
            "suspicious_ua_patterns": []
        },
        
        # Clean honeypot data (no triggers)
        "honeypot_data": {
            "hidden_honeypot_field": "",
            "enhanced_css_hidden_triggered": False,
            "fake_submit_clicked": False,
            "js_optional_field": "",
            "js_optional_field_triggered": False,
            "js_enabled": True,
            "focus_trail": ["name", "email", "aadhaar", "eid", "fathers_name", "phone"],
            "expected_focus_order": ["name", "email", "aadhaar", "eid", "fathers_name", "phone"],
            "focus_order_triggered": False,
            "offscreen_mouse_triggered": False,
            "js_delayed_field_triggered": False,
            "canvas_fingerprint_triggered": False,
            "dom_mutation_triggered": False,
            "dom_stable": True,
            "page_load_duration": 12.5
        },
        
        "metadata": {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "screen_resolution": "1920x1080",
            "timezone": "America/New_York",
            "language": "en-US",
            "platform": "Win32",
            "webdriver_detected": False,
            "plugins_count": 23,
            "mime_types_count": 67,
            "touch_points": 10,
            "hardware_concurrency": 8,
            "device_memory": 16
        }
    }
    
    try:
        print("📤 Sending clean human request...")
        response = requests.post(url, json=payload_human, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Clean Human Response received!")
            
            # Check prediction
            prediction = result.get('prediction', [{}])[0]
            print(f"👤 Bot Detected: {prediction.get('bot', 'Unknown')}")
            print(f"📊 Confidence: {prediction.get('confidence', 'Unknown')}")
            
            # Check honeypot analysis
            honeypot_analysis = result.get('enhanced_analysis', {}).get('honeypot_analysis', {})
            if honeypot_analysis:
                print(f"🍯 Honeypot Analysis:")
                print(f"   • Threat Detected: {honeypot_analysis.get('threat_detected', 'Unknown')}")
                print(f"   • Threat Level: {honeypot_analysis.get('threat_level', 'Unknown')}")
                
                summary = honeypot_analysis.get('honeypot_summary', {})
                if summary:
                    triggered = summary.get('triggered_honeypots', 0)
                    total = summary.get('total_honeypots', 8)
                    print(f"   • Honeypots Triggered: {triggered}/{total}")
            
            print("\n" + "="*60 + "\n")
            
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🍯 8-Layer Honeypot Detection System Test")
    print("="*60)
    print("Testing both bot (multiple triggers) and human (clean) scenarios")
    print("="*60)
    
    test_honeypot_triggers()
    
    print("🏁 Testing complete!")
