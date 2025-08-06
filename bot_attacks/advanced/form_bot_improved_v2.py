#!/usr/bin/env python3
"""
Enhanced Form Bot v2 - More Human-Like Mouse Movement Simulation
This version creates much more realistic mouse movements that closely mimic human behavior
"""

import time
import random
import math
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import numpy as np

class HumanLikeFormBot:
    def __init__(self, headless=False, stealth_mode=True):
        self.setup_driver(headless, stealth_mode)
        self.mouse_movements = []
        self.key_presses = []
        self.session_events = []
        
    def setup_driver(self, headless=False, stealth_mode=True):
        """Setup Chrome driver with human-like configuration"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        if stealth_mode:
            # Make the bot more human-like
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
        
        # Set window size to common resolution
        chrome_options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        if stealth_mode:
            # Execute script to hide webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def bezier_curve_movement(self, start_x, start_y, end_x, end_y, duration=1.0, num_points=50):
        """
        Generate realistic mouse movement using Bezier curves
        This creates smooth, curved paths like humans naturally move
        """
        # Add some randomness to control points for natural variation
        control1_x = start_x + random.uniform(-100, 100)
        control1_y = start_y + random.uniform(-50, 50)
        control2_x = end_x + random.uniform(-100, 100)
        control2_y = end_y + random.uniform(-50, 50)
        
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            
            # Cubic Bezier curve formula
            x = ((1-t)**3 * start_x + 
                 3*(1-t)**2*t * control1_x + 
                 3*(1-t)*t**2 * control2_x + 
                 t**3 * end_x)
            
            y = ((1-t)**3 * start_y + 
                 3*(1-t)**2*t * control1_y + 
                 3*(1-t)*t**2 * control2_y + 
                 t**3 * end_y)
            
            points.append((int(x), int(y)))
        
        return points
    
    def add_mouse_jitter(self, x, y, intensity=2):
        """Add small random movements to simulate natural hand tremor"""
        jitter_x = random.uniform(-intensity, intensity)
        jitter_y = random.uniform(-intensity, intensity)
        return int(x + jitter_x), int(y + jitter_y)
    
    def human_like_timing(self, base_delay=0.1):
        """Generate human-like timing variations"""
        # Humans don't move at constant speeds
        variation = random.uniform(0.5, 2.0)  # 50% to 200% of base delay
        micro_pause = random.uniform(0, 0.05)  # Random micro-pauses
        return base_delay * variation + micro_pause
    
    def simulate_reading_pause(self):
        """Simulate time humans take to read and think"""
        reading_time = random.uniform(1.5, 4.0)  # 1.5 to 4 seconds
        print(f"📖 Simulating reading/thinking pause: {reading_time:.2f}s")
        time.sleep(reading_time)
    
    def move_to_element_naturally(self, element, reading_pause=True):
        """Move to an element using natural human-like movement patterns"""
        if reading_pause:
            self.simulate_reading_pause()
        
        # Get current mouse position (approximate)
        current_x = random.randint(100, 800)
        current_y = random.randint(100, 600)
        
        # Get target element position
        target_x = element.location['x'] + element.size['width'] // 2
        target_y = element.location['y'] + element.size['height'] // 2
        
        # Add some randomness to target position
        target_x += random.randint(-10, 10)
        target_y += random.randint(-5, 5)
        
        print(f"🖱️ Moving from ({current_x}, {current_y}) to ({target_x}, {target_y})")
        
        # Generate curved path
        movement_duration = random.uniform(0.8, 2.0)
        num_points = random.randint(40, 80)  # More points = smoother movement
        
        path_points = self.bezier_curve_movement(
            current_x, current_y, target_x, target_y, 
            movement_duration, num_points
        )
        
        # Execute movement along the path
        actions = ActionChains(self.driver)
        
        for i, (x, y) in enumerate(path_points):
            # Add jitter for realism
            jittered_x, jittered_y = self.add_mouse_jitter(x, y)
            
            # Move to position
            actions.move_by_offset(jittered_x - current_x, jittered_y - current_y)
            current_x, current_y = jittered_x, jittered_y
            
            # Record movement
            self.record_mouse_event('mousemove', current_x, current_y)
            
            # Variable timing between movements
            if i % 3 == 0:  # Execute in small batches for smoother movement
                actions.perform()
                actions = ActionChains(self.driver)
                time.sleep(self.human_like_timing(0.02))
        
        # Final move to exact target and click
        actions.move_to_element(element)
        actions.perform()
        
        # Small pause before clicking (humans don't click immediately)
        time.sleep(random.uniform(0.1, 0.3))
    
    def generate_scroll_movements(self, scroll_amount=3):
        """Generate realistic scrolling behavior with mouse movements"""
        print("📜 Generating natural scrolling movements...")
        
        for _ in range(scroll_amount):
            # Move mouse to random scroll position
            scroll_x = random.randint(400, 1200)
            scroll_y = random.randint(300, 700)
            
            # Move to scroll position naturally
            self.move_mouse_to_position(scroll_x, scroll_y, quick=True)
            
            # Scroll with some variation
            scroll_delta = random.randint(100, 300)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_delta});")
            
            # Record scroll event
            self.record_mouse_event('scroll', scroll_x, scroll_y)
            
            # Pause between scrolls
            time.sleep(random.uniform(0.5, 1.5))
    
    def move_mouse_to_position(self, x, y, quick=False):
        """Move mouse to specific position with natural movement"""
        current_x = random.randint(100, 800)
        current_y = random.randint(100, 600)
        
        duration = random.uniform(0.3, 0.8) if quick else random.uniform(0.8, 1.5)
        points = random.randint(15, 30) if quick else random.randint(30, 50)
        
        path = self.bezier_curve_movement(current_x, current_y, x, y, duration, points)
        
        actions = ActionChains(self.driver)
        for px, py in path[::2]:  # Skip some points for performance
            jx, jy = self.add_mouse_jitter(px, py)
            actions.move_by_offset(jx - current_x, jy - current_y)
            current_x, current_y = jx, jy
            self.record_mouse_event('mousemove', current_x, current_y)
        
        actions.perform()
    
    def type_like_human(self, element, text):
        """Type text with human-like patterns"""
        element.clear()
        time.sleep(random.uniform(0.2, 0.5))
        
        for i, char in enumerate(text):
            element.send_keys(char)
            self.record_key_event('keypress', char)
            
            # Variable typing speed
            if char == ' ':
                # Longer pause after spaces
                time.sleep(random.uniform(0.1, 0.3))
            elif char in '.,!?':
                # Pause after punctuation
                time.sleep(random.uniform(0.2, 0.4))
            else:
                # Normal character delay with variation
                base_delay = random.uniform(0.05, 0.15)
                # Occasionally pause longer (thinking)
                if random.random() < 0.1:
                    base_delay += random.uniform(0.5, 1.0)
                time.sleep(base_delay)
            
            # Occasionally make "typos" and correct them
            if random.random() < 0.03 and i < len(text) - 1:  # 3% chance
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.send_keys(wrong_char)
                time.sleep(random.uniform(0.2, 0.5))
                element.send_keys('\b')  # Backspace
                time.sleep(random.uniform(0.1, 0.3))
    
    def generate_idle_movements(self, duration=3.0):
        """Generate random mouse movements when "thinking" or reading"""
        print("💭 Generating idle thinking movements...")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # Small random movements
            x = random.randint(300, 1200)
            y = random.randint(200, 800)
            
            self.move_mouse_to_position(x, y, quick=True)
            time.sleep(random.uniform(0.3, 0.8))
            
            # Occasionally move mouse to edges (common human behavior)
            if random.random() < 0.3:
                edge_x = random.choice([50, 1850])  # Left or right edge
                edge_y = random.randint(200, 800)
                self.move_mouse_to_position(edge_x, edge_y, quick=True)
                time.sleep(random.uniform(0.2, 0.5))
    
    def record_mouse_event(self, event_type, x, y):
        """Record mouse events for analysis"""
        event = {
            'event_name': event_type,
            'x_position': x,
            'y_position': y,
            'timestamp': int(time.time() * 1000)
        }
        self.session_events.append(event)
        self.mouse_movements.append(event)
    
    def record_key_event(self, event_type, key):
        """Record keyboard events"""
        event = {
            'event_name': event_type,
            'key': key,
            'timestamp': int(time.time() * 1000)
        }
        self.session_events.append(event)
        self.key_presses.append(event)
    
    def fill_form_naturally(self, url="http://localhost:3000/register"):
        """Fill out the form with extremely natural human behavior"""
        print("🚀 Starting Enhanced Human-Like Form Bot v2")
        print("🎯 Target:", url)
        
        try:
            # Navigate to the form
            print("📱 Navigating to form...")
            self.driver.get(url)
            time.sleep(random.uniform(2.0, 4.0))  # Page load + initial scan time
            
            # Generate some initial exploratory movements
            print("👀 Initial page exploration...")
            self.generate_idle_movements(duration=2.0)
            
            # Scroll around to "read" the page
            self.generate_scroll_movements(scroll_amount=2)
            
            # Wait for form to be fully loaded
            wait = WebDriverWait(self.driver, 10)
            
            # Generate realistic form data
            form_data = {
                'name': random.choice(['John Smith', 'Alice Johnson', 'Bob Wilson', 'Sarah Davis', 'Mike Brown']),
                'email': f"{random.choice(['john', 'alice', 'bob', 'sarah', 'mike'])}{random.randint(100, 999)}@gmail.com",
                'fathers_name': random.choice(['Robert Smith', 'David Johnson', 'James Wilson', 'William Davis', 'Thomas Brown']),
                'aadhaar': ''.join([str(random.randint(0, 9)) for _ in range(14)]),
                'eid': ''.join([str(random.randint(0, 9)) for _ in range(12)]),
                'phone': f"9{random.randint(100000000, 999999999)}"
            }
            
            print("📝 Filling form with realistic human behavior...")
            
            # Fill each field with natural behavior
            field_selectors = [
                ('name', 'input[name="name"]'),
                ('email', 'input[name="email"]'),
                ('fathers_name', 'input[name="fathers_name"]'),
                ('aadhaar', 'input[name="aadhaar"]'),
                ('eid', 'input[name="eid"]'),
                ('phone', 'input[name="phone"]')
            ]
            
            for field_name, selector in field_selectors:
                try:
                    print(f"📝 Filling {field_name}...")
                    
                    # Some idle movement before focusing on field
                    self.generate_idle_movements(duration=random.uniform(1.0, 2.0))
                    
                    # Find and move to field naturally
                    field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    self.move_to_element_naturally(field, reading_pause=True)
                    
                    # Click the field
                    field.click()
                    self.record_mouse_event('click', 
                                          field.location['x'] + field.size['width']//2,
                                          field.location['y'] + field.size['height']//2)
                    
                    # Small pause after click
                    time.sleep(random.uniform(0.2, 0.5))
                    
                    # Type naturally
                    self.type_like_human(field, form_data[field_name])
                    
                    # Sometimes move mouse away after typing (natural behavior)
                    if random.random() < 0.4:
                        away_x = random.randint(400, 1000)
                        away_y = random.randint(300, 700)
                        self.move_mouse_to_position(away_x, away_y, quick=True)
                    
                    print(f"✅ {field_name}: {form_data[field_name]}")
                    
                except Exception as e:
                    print(f"❌ Error filling {field_name}: {e}")
                    continue
            
            # Final review behavior - move around form
            print("🔍 Final form review...")
            self.generate_idle_movements(duration=random.uniform(2.0, 4.0))
            
            # Move to submit button naturally
            print("🎯 Moving to submit button...")
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            self.move_to_element_naturally(submit_button, reading_pause=True)
            
            # Pause before submitting (humans often hesitate)
            hesitation_time = random.uniform(1.0, 3.0)
            print(f"🤔 Final hesitation: {hesitation_time:.2f}s")
            time.sleep(hesitation_time)
            
            # Submit the form
            print("📤 Submitting form...")
            submit_button.click()
            self.record_mouse_event('click', 
                                  submit_button.location['x'] + submit_button.size['width']//2,
                                  submit_button.location['y'] + submit_button.size['height']//2)
            
            # Wait to see response
            time.sleep(5.0)
            
            # Print statistics
            print(f"\n📊 Session Statistics:")
            print(f"   🖱️ Mouse movements: {len(self.mouse_movements)}")
            print(f"   ⌨️ Key presses: {len(self.key_presses)}")
            print(f"   📝 Total events: {len(self.session_events)}")
            print(f"   ⏱️ Session duration: {len(self.session_events) * 0.1:.1f}s (estimated)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during form filling: {e}")
            return False
        
        finally:
            time.sleep(2)
            self.driver.quit()

def main():
    """Run the enhanced human-like form bot"""
    print("🤖 Enhanced Human-Like Form Bot v2")
    print("=" * 50)
    
    # Create bot instance
    bot = HumanLikeFormBot(headless=False, stealth_mode=True)
    
    try:
        # Fill the form
        success = bot.fill_form_naturally()
        
        if success:
            print("✅ Form filled successfully with human-like behavior!")
        else:
            print("❌ Form filling failed")
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
