#!/usr/bin/env python3
"""
Test the Enhanced Honeypot System
Tests the 3-layer honeypot detection with various scenarios
"""

import sys
import os
import json
from datetime import datetime

# Add the backend path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'api'))

try:
    from modules.honeypot import HoneypotModule
    print("✅ Successfully imported HoneypotModule")
except ImportError as e:
    print(f"❌ Failed to import HoneypotModule: {e}")
    sys.exit(1)

def test_honeypot_scenarios():
    """Test various honeypot detection scenarios"""
    
    honeypot = HoneypotModule()
    print(f"\n🍯 Testing Enhanced Honeypot Module v{honeypot.version}")
    print("=" * 50)
    
    # Test 1: Clean user (no honeypots triggered)
    print("\n📝 Test 1: Clean User - No Honeypots Triggered")
    clean_events = [
        {'event_name': 'mousemove', 'x_position': 100, 'y_position': 50, 'timestamp': 1000},
        {'event_name': 'click', 'x_position': 200, 'y_position': 100, 'timestamp': 1500},
        {'event_name': 'keypress', 'x_position': 0, 'y_position': 0, 'timestamp': 2000}
    ]
    clean_metadata = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'hidden_honeypot_field': '',
        'fake_submit_clicked': False,
        'js_optional_field': '',
        'js_enabled': True
    }
    
    result = honeypot.analyze(clean_events, clean_metadata)
    print(f"  Bot Detected: {result['honeypot_verdict']['is_bot']}")
    print(f"  Threat Level: {result['analysis']['threat_level']}")
    print(f"  Honeypot Score: {result['analysis']['honeypot_score']:.3f}")
    print(f"  Honeypots Triggered: {result['honeypot_summary']['triggered_honeypots']}/3")
    
    # Test 2: Hidden field filled (strongest indicator)
    print("\n📝 Test 2: Bot - Hidden CSS Field Filled")
    bot_metadata_hidden = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'hidden_honeypot_field': 'https://example.com',  # Bot filled this field
        'fake_submit_clicked': False,
        'js_optional_field': '',
        'js_enabled': True
    }
    
    result = honeypot.analyze(clean_events, bot_metadata_hidden)
    print(f"  Bot Detected: {result['honeypot_verdict']['is_bot']}")
    print(f"  Threat Level: {result['analysis']['threat_level']}")
    print(f"  Honeypot Score: {result['analysis']['honeypot_score']:.3f}")
    print(f"  Honeypots Triggered: {result['honeypot_summary']['triggered_honeypots']}/3")
    print(f"  Triggered Types: {result['honeypot_summary']['honeypot_types_triggered']}")
    
    # Test 3: Fake submit button clicked
    print("\n📝 Test 3: Bot - Fake Submit Button Clicked")
    bot_metadata_fake_submit = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'hidden_honeypot_field': '',
        'fake_submit_clicked': True,  # Bot clicked fake submit
        'js_optional_field': '',
        'js_enabled': True
    }
    
    result = honeypot.analyze(clean_events, bot_metadata_fake_submit)
    print(f"  Bot Detected: {result['honeypot_verdict']['is_bot']}")
    print(f"  Threat Level: {result['analysis']['threat_level']}")
    print(f"  Honeypot Score: {result['analysis']['honeypot_score']:.3f}")
    print(f"  Honeypots Triggered: {result['honeypot_summary']['triggered_honeypots']}/3")
    
    # Test 4: JS field filled without JS
    print("\n📝 Test 4: Bot - JS Field Filled Without JavaScript")
    bot_metadata_js = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'hidden_honeypot_field': '',
        'fake_submit_clicked': False,
        'js_optional_field': 'Additional info',  # Bot filled JS field
        'js_enabled': False  # But JS is disabled
    }
    
    result = honeypot.analyze(clean_events, bot_metadata_js)
    print(f"  Bot Detected: {result['honeypot_verdict']['is_bot']}")
    print(f"  Threat Level: {result['analysis']['threat_level']}")
    print(f"  Honeypot Score: {result['analysis']['honeypot_score']:.3f}")
    print(f"  Honeypots Triggered: {result['honeypot_summary']['triggered_honeypots']}/3")
    
    # Test 5: Multiple honeypots triggered (critical threat)
    print("\n📝 Test 5: Bot - Multiple Honeypots Triggered")
    bot_metadata_multiple = {
        'user_agent': 'HeadlessChrome/91.0.4472.77',
        'hidden_honeypot_field': 'http://bot-site.com',
        'fake_submit_clicked': True,
        'js_optional_field': 'Bot filled this',
        'js_enabled': False
    }
    
    result = honeypot.analyze([], bot_metadata_multiple)  # No events (suspicious)
    print(f"  Bot Detected: {result['honeypot_verdict']['is_bot']}")
    print(f"  Threat Level: {result['analysis']['threat_level']}")
    print(f"  Honeypot Score: {result['analysis']['honeypot_score']:.3f}")
    print(f"  Total Score: {result['analysis']['total_score']:.3f}")
    print(f"  Honeypots Triggered: {result['honeypot_summary']['triggered_honeypots']}/3")
    print(f"  Triggered Types: {result['honeypot_summary']['honeypot_types_triggered']}")
    
    # Test 6: Test honeypot field configurations
    print("\n📝 Test 6: Honeypot Field Configurations")
    fields = honeypot.get_honeypot_fields()
    print("  Available honeypot fields:")
    for field_type, config in fields.items():
        print(f"    • {field_type}: {config['name']} ({config['type']})")
    
    # Test 7: Module information
    print("\n📝 Test 7: Module Information")
    info = honeypot.get_info()
    print(f"  Module: {info['module']} v{info['version']}")
    print(f"  Honeypot Types: {info['honeypot_types']}")
    print(f"  Weights: {info['honeypot_weights']}")
    print(f"  Threshold: {info['suspicious_threshold']}")

if __name__ == "__main__":
    test_honeypot_scenarios()
    print("\n✅ All honeypot tests completed!")
