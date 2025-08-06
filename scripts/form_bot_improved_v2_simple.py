#!/usr/bin/env python3
"""
Enhanced Form Bot v2 - Simplified Robust Version
This version focuses on reliability while still generating more human-like movements
"""

import time
import random
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

class SimpleHumanLikeBot:
    def __init__(self, headless=False):
        self.setup_driver(headless)
        self.mouse_movements = []
        self.key_presses = []
        self.session_events = []
        
    def setup_driver(self, headless=False):
        """Setup Chrome driver with simple but effective configuration"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        # Basic stealth settings
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set a normal user agent
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
        
        # Set window size
        chrome_options.add_argument('--window-size=1280,720')
        
        # Disable various automation detection features
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        
        # Hide webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Get window size for safe operations
        size = self.driver.get_window_size()
        self.window_width = size['width']
        self.window_height = size['height']
        print(f"🖥️ Browser window: {self.window_width}x{self.window_height}")
    
    def record_mouse_event(self, event_type, x=0, y=0):
        """Record mouse events for analysis"""
        event = {
            'event_name': event_type,
            'x_position': x,
            'y_position': y,
            'timestamp': int(time.time() * 1000)
        }
        self.session_events.append(event)
        self.mouse_movements.append(event)
    
    def record_key_event(self, event_type, key=''):
        """Record keyboard events"""
        event = {
            'event_name': event_type,
            'key': key,
            'timestamp': int(time.time() * 1000)
        }
        self.session_events.append(event)
        self.key_presses.append(event)
    
    def human_pause(self, min_time=0.5, max_time=2.0):
        """Simple human-like pause"""
        pause_time = random.uniform(min_time, max_time)
        time.sleep(pause_time)
    
    def generate_mouse_movements_around_element(self, element, count=20):
        """Generate mouse movements around an element without complex paths"""
        try:
            # Get element position safely
            location = element.location
            size = element.size
            
            center_x = location['x'] + size['width'] // 2
            center_y = location['y'] + size['height'] // 2
            
            # Generate simple movements around the element
            for i in range(count):
                # Small random movements around the element
                offset_x = random.randint(-50, 50)
                offset_y = random.randint(-30, 30)
                
                # Use JavaScript to simulate mouse movement
                self.driver.execute_script(f"""
                    var event = new MouseEvent('mousemove', {{
                        bubbles: true,
                        cancelable: true,
                        view: window
                    }});
                    document.dispatchEvent(event);
                """)
                
                # Record the movement
                self.record_mouse_event('mousemove', center_x + offset_x, center_y + offset_y)
                
                # Small pause between movements
                time.sleep(random.uniform(0.01, 0.05))
                
        except Exception as e:
            print(f"⚠️ Movement generation warning: {e}")
    
    def type_like_human(self, element, text):
        """Type text with human-like patterns"""
        try:
            element.clear()
            self.human_pause(0.2, 0.5)
            
            for i, char in enumerate(text):
                element.send_keys(char)
                self.record_key_event('keypress', char)
                
                # Variable typing speed
                if char == ' ':
                    time.sleep(random.uniform(0.1, 0.2))
                elif char in '.,!?':
                    time.sleep(random.uniform(0.15, 0.3))
                else:
                    time.sleep(random.uniform(0.05, 0.12))
                
                # Occasional longer pause (thinking)
                if random.random() < 0.08:
                    time.sleep(random.uniform(0.3, 0.8))
                    
        except Exception as e:
            print(f"⚠️ Typing error: {e}")
    
    def move_to_element_and_click(self, element, field_name="element"):
        """Safely move to element and click with mouse movement generation"""
        try:
            print(f"🎯 Moving to {field_name}...")
            
            # Generate some movements before focusing on the element
            self.generate_mouse_movements_around_element(element, count=random.randint(15, 25))
            
            # Reading/thinking pause
            self.human_pause(1.0, 2.5)
            
            # More movements while "considering" the field
            self.generate_mouse_movements_around_element(element, count=random.randint(10, 20))
            
            # Scroll element into view if needed
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            
            # Generate movements after scroll
            self.generate_mouse_movements_around_element(element, count=random.randint(8, 15))
            
            # Wait for element to be clickable
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(element))
            
            # Click the element
            element.click()
            
            # Record click
            location = element.location
            size = element.size
            click_x = location['x'] + size['width'] // 2
            click_y = location['y'] + size['height'] // 2
            self.record_mouse_event('click', click_x, click_y)
            
            # Pause after click
            self.human_pause(0.2, 0.5)
            
            return True
            
        except Exception as e:
            print(f"❌ Error with {field_name}: {e}")
            return False
    
    def generate_page_exploration(self):
        """Generate exploration movements without complex coordinates"""
        print("👀 Exploring page...")
        
        try:
            # Simple scroll movements
            for _ in range(random.randint(2, 4)):
                scroll_amount = random.randint(100, 300)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                self.record_mouse_event('scroll', 0, 0)
                time.sleep(random.uniform(0.5, 1.2))
            
            # Generate some random mouse events using JavaScript
            for _ in range(random.randint(30, 60)):
                self.driver.execute_script("""
                    var event = new MouseEvent('mousemove', {
                        bubbles: true,
                        cancelable: true,
                        view: window
                    });
                    document.dispatchEvent(event);
                """)
                self.record_mouse_event('mousemove', 
                                      random.randint(100, 800), 
                                      random.randint(100, 500))
                time.sleep(random.uniform(0.02, 0.08))
                
        except Exception as e:
            print(f"⚠️ Exploration warning: {e}")
    
    def fill_form_naturally(self, url="http://localhost:3000/register"):
        """Fill out the form with human-like behavior"""
        print("🚀 Starting Enhanced Human-Like Form Bot v2 (Simplified)")
        print("🎯 Target:", url)
        
        try:
            # Navigate to the form
            print("📱 Navigating to form...")
            self.driver.get(url)
            self.human_pause(2.0, 4.0)
            
            # Initial page exploration
            self.generate_page_exploration()
            
            # Wait for form to be ready
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
            
            print("📝 Filling form with realistic behavior...")
            
            # Fill each field
            field_configs = [
                ('name', 'input[name="name"]', 'Name field'),
                ('email', 'input[name="email"]', 'Email field'),
                ('fathers_name', 'input[name="fathers_name"]', 'Father\'s name field'),
                ('aadhaar', 'input[name="aadhaar"]', 'Aadhaar field'),
                ('eid', 'input[name="eid"]', 'EID field'),
                ('phone', 'input[name="phone"]', 'Phone field')
            ]
            
            successful_fields = 0
            
            for field_name, selector, description in field_configs:
                try:
                    print(f"📝 Processing {description}...")
                    
                    # Find the field
                    field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    
                    # Move to and click field
                    if self.move_to_element_and_click(field, description):
                        # Type the data
                        self.type_like_human(field, form_data[field_name])
                        print(f"✅ {field_name}: {form_data[field_name]}")
                        successful_fields += 1
                        
                        # Some idle time after filling
                        self.human_pause(0.5, 1.5)
                    
                except Exception as e:
                    print(f"❌ Error with {description}: {e}")
                    continue
            
            if successful_fields == 0:
                print("❌ No fields were filled successfully")
                return False
            
            # HONEYPOT TRIGGER: Simple version should trigger the hidden CSS field
            print("🍯 Simple bot triggering honeypot: Hidden CSS field")
            try:
                # Find and fill the hidden honeypot field
                hidden_field = self.driver.find_element(By.ID, 'website_url')
                hidden_field.send_keys('http://simple-bot-detected.com')
                print("✅ Hidden honeypot field filled successfully")
                self.human_pause(0.3, 0.7)
            except Exception as e:
                print(f"⚠️ Could not trigger hidden honeypot: {e}")

            # Final form review
            print("🔍 Final form review...")
            self.human_pause(2.0, 4.0)
            
            # Generate some final movements
            for _ in range(random.randint(20, 40)):
                self.driver.execute_script("""
                    var event = new MouseEvent('mousemove', {
                        bubbles: true,
                        cancelable: true,
                        view: window
                    });
                    document.dispatchEvent(event);
                """)
                self.record_mouse_event('mousemove', 
                                      random.randint(200, 700), 
                                      random.randint(200, 500))
                time.sleep(random.uniform(0.03, 0.1))
            
            # Find and click submit button
            print("🎯 Submitting form...")
            try:
                submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
                
                if self.move_to_element_and_click(submit_button, "Submit button"):
                    print("📤 Form submitted!")
                    
                    # Wait to see response
                    time.sleep(5.0)
                    
                    # Print statistics
                    print(f"\n📊 Session Statistics:")
                    print(f"   🖱️ Mouse movements: {len(self.mouse_movements)}")
                    print(f"   ⌨️ Key presses: {len(self.key_presses)}")
                    print(f"   📝 Total events: {len(self.session_events)}")
                    print(f"   ✅ Fields filled: {successful_fields}/6")
                    
                    return True
                else:
                    print("❌ Could not click submit button")
                    return False
                    
            except Exception as e:
                print(f"❌ Submit error: {e}")
                return False
            
        except Exception as e:
            print(f"❌ Critical error: {e}")
            return False
        
        finally:
            self.human_pause(2.0, 3.0)
            try:
                self.driver.quit()
            except:
                pass

def main():
    """Run the simplified human-like form bot"""
    print("🤖 Enhanced Human-Like Form Bot v2 (Simplified & Robust)")
    print("=" * 60)
    
    try:
        # Create bot instance
        bot = SimpleHumanLikeBot(headless=False)
        
        # Fill the form
        success = bot.fill_form_naturally()
        
        if success:
            print("✅ Form filled successfully with human-like behavior!")
        else:
            print("❌ Form filling encountered issues")
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
