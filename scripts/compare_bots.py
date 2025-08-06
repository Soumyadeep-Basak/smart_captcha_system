#!/usr/bin/env python3
"""
Bot Movement Pattern Comparison Tool
Run this to compare movement patterns between different bot versions
"""

import subprocess
import sys
import time

def run_bot_version(script_name, description):
    """Run a specific bot version and capture output"""
    print(f"\n{'='*60}")
    print(f"🤖 Running {description}")
    print(f"📁 Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        # Run the bot script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=120)
        
        print("📊 Output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Errors:")
            print(result.stderr)
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ Bot timed out after 2 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        return False

def main():
    """Compare different bot versions"""
    print("🔬 Bot Movement Pattern Comparison Tool")
    print("This will run different bot versions to compare their behavior")
    
    bots_to_test = [
        ("form_bot.py", "Original Form Bot"),
        ("form_bot_improved_v2.py", "Enhanced Human-Like Bot v2")
    ]
    
    results = {}
    
    for script, description in bots_to_test:
        print(f"\n⏳ Preparing to run {description}...")
        time.sleep(2)
        
        success = run_bot_version(script, description)
        results[description] = success
        
        print(f"✅ {description}: {'SUCCESS' if success else 'FAILED'}")
        
        # Wait between tests
        if script != bots_to_test[-1][0]:  # Not the last one
            print("\n⏸️ Waiting 5 seconds before next test...")
            time.sleep(5)
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 COMPARISON SUMMARY")
    print(f"{'='*60}")
    
    for bot_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{bot_name:30} | {status}")
    
    print(f"\n💡 To view detailed movement patterns, check:")
    print(f"   - Admin dashboard: http://localhost:3000/admin")
    print(f"   - Browser console logs during bot execution")
    print(f"   - Backend API logs")

if __name__ == "__main__":
    main()
