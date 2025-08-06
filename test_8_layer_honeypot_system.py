#!/usr/bin/env python3
"""
Test script for 8-Layer Honeypot System
Tests both bot scripts against the new enhanced honeypot detection
"""

import subprocess
import time
import requests
import json
from datetime import datetime

def test_api_health():
    """Test if the API is running and healthy"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API Health Check Passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Architecture: {data.get('architecture')}")
            modules = data.get('modules', {})
            for module_name, module_info in modules.items():
                print(f"   {module_name}: {module_info.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ API Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health Check Failed: {e}")
        return False

def get_recent_predictions():
    """Get the most recent predictions from the API"""
    try:
        response = requests.get('http://localhost:5000/predictions', timeout=10)
        if response.status_code == 200:
            predictions = response.json()
            return predictions[:3]  # Get last 3 predictions
        else:
            print(f"⚠️ Could not fetch predictions: {response.status_code}")
            return []
    except Exception as e:
        print(f"⚠️ Error fetching predictions: {e}")
        return []

def analyze_honeypot_results(predictions):
    """Analyze honeypot detection results"""
    print("\n🍯 HONEYPOT ANALYSIS RESULTS:")
    print("=" * 60)
    
    for i, pred in enumerate(predictions, 1):
        print(f"\nPrediction {i}:")
        print(f"  🤖 Bot Detected: {pred.get('isBot', 'Unknown')}")
        print(f"  📅 Timestamp: {pred.get('timestamp', 'Unknown')}")
        print(f"  🌐 IP: {pred.get('ipAddress', 'Unknown')}")
        
        enhanced_analysis = pred.get('enhanced_analysis', {})
        honeypot_analysis = enhanced_analysis.get('honeypot_analysis', {})
        
        if honeypot_analysis:
            print(f"  🚨 Threat Detected: {honeypot_analysis.get('threat_detected', False)}")
            print(f"  📊 Threat Level: {honeypot_analysis.get('threat_level', 'unknown')}")
            print(f"  🎯 Honeypot Score: {honeypot_analysis.get('honeypot_score', 0):.3f}")
            print(f"  🔍 Confidence: {honeypot_analysis.get('confidence', 0):.3f}")
            
            honeypot_summary = honeypot_analysis.get('honeypot_summary', {})
            triggered = honeypot_summary.get('triggered_honeypots', 0)
            total = honeypot_summary.get('total_honeypots', 8)
            print(f"  🍯 Honeypots Triggered: {triggered}/{total}")
            
            # Show individual honeypot results
            honeypot_details = honeypot_analysis.get('honeypot_details', {})
            detailed_results = honeypot_details.get('detailed_results', {})
            
            if detailed_results:
                print(f"  📋 Individual Honeypot Results:")
                for honeypot_name, details in detailed_results.items():
                    triggered = details.get('triggered', False)
                    score = details.get('score', 0)
                    status = "🚨 TRIGGERED" if triggered else "✅ CLEAN"
                    print(f"    • {honeypot_name}: {status} (Score: {score:.1f})")

def run_bot_test(bot_script, bot_name):
    """Run a specific bot script and analyze results"""
    print(f"\n🤖 TESTING {bot_name.upper()}")
    print("=" * 60)
    
    # Get predictions before test
    initial_predictions = get_recent_predictions()
    initial_count = len(initial_predictions)
    
    print(f"📊 Initial predictions count: {initial_count}")
    print(f"🚀 Running {bot_script}...")
    
    try:
        # Run the bot script
        result = subprocess.run(
            ['python', bot_script], 
            cwd='d:/hack/botv1/scripts',
            capture_output=True, 
            text=True, 
            timeout=120  # 2 minute timeout
        )
        
        if result.returncode == 0:
            print("✅ Bot script completed successfully")
        else:
            print(f"⚠️ Bot script completed with warnings (return code: {result.returncode})")
        
        # Show bot output
        if result.stdout:
            print("📝 Bot Output:")
            print(result.stdout[-500:])  # Last 500 characters
        
        if result.stderr:
            print("⚠️ Bot Errors:")
            print(result.stderr[-300:])  # Last 300 characters
        
    except subprocess.TimeoutExpired:
        print("⏰ Bot script timed out after 2 minutes")
    except Exception as e:
        print(f"❌ Error running bot script: {e}")
    
    # Wait for API to process
    print("⏱️ Waiting 5 seconds for API processing...")
    time.sleep(5)
    
    # Get predictions after test
    final_predictions = get_recent_predictions()
    final_count = len(final_predictions)
    
    print(f"📊 Final predictions count: {final_count}")
    
    if final_count > initial_count:
        print(f"🎯 New predictions detected: {final_count - initial_count}")
        # Analyze the newest predictions (the ones from this bot test)
        new_predictions = final_predictions[:final_count - initial_count]
        analyze_honeypot_results(new_predictions)
    else:
        print("⚠️ No new predictions detected - bot may not have reached the API")
    
    return final_predictions

def main():
    """Main test function"""
    print("🍯 8-LAYER HONEYPOT SYSTEM TEST")
    print("=" * 60)
    print(f"🕒 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check API health first
    if not test_api_health():
        print("❌ API is not healthy. Please start the backend API first:")
        print("   cd backend/api && python app.py")
        return
    
    print("\n✅ API is healthy - proceeding with bot tests...")
    
    # Test bot scripts
    bot_tests = [
        ('form_bot_improved_v2_simple.py', 'Simple Bot (1-2 honeypots)'),
        ('form_bot_improved_v2.py', 'Advanced Bot (6+ honeypots)')
    ]
    
    all_results = []
    
    for bot_script, bot_name in bot_tests:
        try:
            results = run_bot_test(bot_script, bot_name)
            all_results.extend(results)
            
            # Wait between tests
            print(f"\n⏸️ Waiting 10 seconds before next test...")
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n🛑 Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error in bot test: {e}")
            continue
    
    # Final summary
    print("\n📊 FINAL TEST SUMMARY")
    print("=" * 60)
    
    if all_results:
        print(f"Total predictions analyzed: {len(all_results)}")
        
        bot_detected_count = sum(1 for pred in all_results if pred.get('isBot', False))
        human_detected_count = len(all_results) - bot_detected_count
        
        print(f"🤖 Bot detections: {bot_detected_count}")
        print(f"👤 Human detections: {human_detected_count}")
        
        # Honeypot effectiveness
        honeypot_triggers = []
        for pred in all_results:
            enhanced = pred.get('enhanced_analysis', {})
            honeypot = enhanced.get('honeypot_analysis', {})
            summary = honeypot.get('honeypot_summary', {})
            triggered = summary.get('triggered_honeypots', 0)
            honeypot_triggers.append(triggered)
        
        if honeypot_triggers:
            avg_triggers = sum(honeypot_triggers) / len(honeypot_triggers)
            max_triggers = max(honeypot_triggers)
            print(f"🍯 Average honeypots triggered: {avg_triggers:.1f}/8")
            print(f"🍯 Maximum honeypots triggered: {max_triggers}/8")
        
        print("\n✅ 8-Layer Honeypot System test completed!")
    else:
        print("⚠️ No predictions to analyze")
    
    print(f"🕒 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
