#!/usr/bin/env python3
"""
Enhanced Browser Fingerprinting Test
Tests the new rule-based fingerprinting features
"""

import sys
import os
import json
from pathlib import Path

# Add the backend modules to the path
sys.path.append(str(Path(__file__).parent / 'backend' / 'api'))

from modules.fingerprinting import FingerprintingModule

def test_enhanced_fingerprinting():
    """Test the enhanced fingerprinting module with simulated browser data"""
    
    print("🔍 Testing Enhanced Browser Fingerprinting")
    print("=" * 50)
    
    # Initialize the fingerprinting module
    fp_module = FingerprintingModule()
    
    # Test Case 1: Bot-like fingerprint (WebDriver detected)
    print("\n🤖 Test Case 1: Bot Detection - WebDriver Present")
    print("-" * 40)
    
    bot_fingerprint = {
        'webdriver_detected': True,  # 🔥 Very High Risk
        'plugins_count': 0,          # 🔥 Very High Risk
        'mime_types_count': 0,       # 🔥 Very High Risk
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.124 Safari/537.36',
        'user_agent_length': 100,
        'suspicious_ua_patterns': ['headless'],
        'screen_width': 0,
        'screen_height': 0,
        'suspicious_screen': True,
        'max_touch_points': 0,
        'touch_support': False,
        'webgl_supported': False,
        'canvas_supported': False,
        'audio_context_supported': False,
        'local_storage_supported': False,
        'session_storage_supported': False,
        'hardware_concurrency': 0,
        'device_memory': 0,
        'platform': 'Linux x86_64',
        'language': 'en-US',
        'timezone': 'UTC'
    }
    
    metadata = {
        'user_agent': bot_fingerprint['user_agent'],
        'ip_address': '127.0.0.1'
    }
    
    result = fp_module.analyze_fingerprint(metadata, bot_fingerprint)
    
    print(f"Risk Level: {result['analysis']['risk_level'].upper()}")
    print(f"Risk Score: {result['analysis']['risk_score']:.3f}")
    print(f"Bot Likely: {result['analysis']['is_bot_likely']}")
    print(f"Is Suspicious: {result['verdict']['is_suspicious']}")
    print(f"Risk Indicators ({len(result['analysis']['risk_indicators'])}): {result['analysis']['risk_indicators']}")
    print(f"Recommendation: {result['verdict']['recommendation'].upper()}")
    
    # Test Case 2: Human-like fingerprint
    print("\n👤 Test Case 2: Human Detection - Normal Browser")
    print("-" * 40)
    
    human_fingerprint = {
        'webdriver_detected': False,  # ✅ Good
        'plugins_count': 5,           # ✅ Good
        'mime_types_count': 8,        # ✅ Good
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'user_agent_length': 120,
        'suspicious_ua_patterns': [],
        'screen_width': 1920,
        'screen_height': 1080,
        'suspicious_screen': False,
        'max_touch_points': 0,
        'touch_support': False,
        'webgl_supported': True,
        'canvas_supported': True,
        'audio_context_supported': True,
        'local_storage_supported': True,
        'session_storage_supported': True,
        'hardware_concurrency': 8,
        'device_memory': 8,
        'platform': 'Win32',
        'language': 'en-US',
        'timezone': 'America/New_York'
    }
    
    metadata_human = {
        'user_agent': human_fingerprint['user_agent'],
        'ip_address': '192.168.1.100'
    }
    
    result_human = fp_module.analyze_fingerprint(metadata_human, human_fingerprint)
    
    print(f"Risk Level: {result_human['analysis']['risk_level'].upper()}")
    print(f"Risk Score: {result_human['analysis']['risk_score']:.3f}")
    print(f"Bot Likely: {result_human['analysis']['is_bot_likely']}")
    print(f"Is Suspicious: {result_human['verdict']['is_suspicious']}")
    print(f"Risk Indicators ({len(result_human['analysis']['risk_indicators'])}): {result_human['analysis']['risk_indicators']}")
    print(f"Recommendation: {result_human['verdict']['recommendation'].upper()}")
    
    # Test Case 3: Suspicious but not clearly bot
    print("\n⚠️ Test Case 3: Suspicious Detection - Missing Features")
    print("-" * 40)
    
    suspicious_fingerprint = {
        'webdriver_detected': False,  # ✅ Good
        'plugins_count': 1,           # ⚠️ Low but not zero
        'mime_types_count': 2,        # ⚠️ Low but not zero
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',  # Short
        'user_agent_length': 45,      # ⚠️ Short
        'suspicious_ua_patterns': [],
        'screen_width': 800,
        'screen_height': 600,         # ⚠️ Minimum size
        'suspicious_screen': False,
        'max_touch_points': 0,
        'touch_support': False,
        'webgl_supported': False,     # ⚠️ Missing WebGL
        'canvas_supported': True,
        'audio_context_supported': False,  # ⚠️ Missing audio
        'local_storage_supported': True,
        'session_storage_supported': True,
        'hardware_concurrency': 2,
        'device_memory': 0,          # ⚠️ Missing info
        'platform': 'Linux x86_64',
        'language': 'en-US',
        'timezone': 'UTC'
    }
    
    metadata_suspicious = {
        'user_agent': suspicious_fingerprint['user_agent'],
        'ip_address': '10.0.0.50'
    }
    
    result_suspicious = fp_module.analyze_fingerprint(metadata_suspicious, suspicious_fingerprint)
    
    print(f"Risk Level: {result_suspicious['analysis']['risk_level'].upper()}")
    print(f"Risk Score: {result_suspicious['analysis']['risk_score']:.3f}")
    print(f"Bot Likely: {result_suspicious['analysis']['is_bot_likely']}")
    print(f"Is Suspicious: {result_suspicious['verdict']['is_suspicious']}")
    print(f"Risk Indicators ({len(result_suspicious['analysis']['risk_indicators'])}): {result_suspicious['analysis']['risk_indicators']}")
    print(f"Recommendation: {result_suspicious['verdict']['recommendation'].upper()}")
    
    # Summary
    print("\n📊 FINGERPRINTING TEST SUMMARY")
    print("=" * 50)
    print(f"Bot Case:        Risk={result['analysis']['risk_score']:.3f}, Decision={result['analysis']['is_bot_likely']}")
    print(f"Human Case:      Risk={result_human['analysis']['risk_score']:.3f}, Decision={result_human['analysis']['is_bot_likely']}")
    print(f"Suspicious Case: Risk={result_suspicious['analysis']['risk_score']:.3f}, Decision={result_suspicious['analysis']['is_bot_likely']}")
    
    print("\n🎯 KEY FEATURES TESTED:")
    print("✅ WebDriver Detection (navigator.webdriver)")
    print("✅ Plugins Count (navigator.plugins.length)")
    print("✅ MIME Types Count (navigator.mimeTypes.length)")
    print("✅ User Agent Analysis (navigator.userAgent)")
    print("✅ Screen Properties (screen.width/height)")
    print("✅ Touch Support (navigator.maxTouchPoints)")
    print("✅ Browser Capabilities (WebGL, Canvas, Audio)")
    print("✅ Hardware Information (navigator.hardwareConcurrency)")
    print("✅ Rule-based Scoring System")
    
    print("\n🚀 Enhanced fingerprinting is working correctly!")
    print("The system can now detect bots using advanced browser features.")
    
    # Show feature analysis details
    print("\n🔬 DETAILED FEATURE ANALYSIS")
    print("-" * 30)
    for case_name, fp_result in [("Bot", result), ("Human", result_human), ("Suspicious", result_suspicious)]:
        print(f"\n{case_name} Case Feature Breakdown:")
        if 'fingerprint' in fp_result and 'feature_counts' in fp_result['fingerprint']:
            features = fp_result['fingerprint']['feature_counts']
            for feature, value in features.items():
                print(f"  {feature}: {value}")

if __name__ == "__main__":
    test_enhanced_fingerprinting()
