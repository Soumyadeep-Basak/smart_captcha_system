#!/usr/bin/env python3
"""
Quick test for Enhanced Form Bot v2
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from form_bot_improved_v2 import HumanLikeFormBot

def test_bot():
    """Test the enhanced bot with safety checks"""
    print("🧪 Testing Enhanced Form Bot v2")
    print("=" * 40)
    
    try:
        # Create bot instance
        bot = HumanLikeFormBot(headless=False, stealth_mode=True)
        
        print(f"✅ Bot initialized successfully")
        print(f"🖥️ Window size: {bot.window_width}x{bot.window_height}")
        
        # Test safe position generation
        for i in range(5):
            x, y = bot.get_safe_random_position()
            print(f"📍 Safe position {i+1}: ({x}, {y})")
        
        # Test bounds checking
        test_coords = [(0, 0), (2000, 2000), (-100, -100), (bot.window_width + 100, bot.window_height + 100)]
        for x, y in test_coords:
            safe_x, safe_y = bot.ensure_bounds(x, y)
            print(f"🛡️ Bounds test: ({x}, {y}) -> ({safe_x}, {safe_y})")
        
        # Run the actual form filling
        print("\n🚀 Starting form filling test...")
        success = bot.fill_form_naturally()
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_bot()
    print(f"\n{'✅ TEST PASSED' if success else '❌ TEST FAILED'}")
