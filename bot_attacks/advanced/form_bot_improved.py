import random
import time
import math
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Set up the WebDriver options
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

# Try to use ChromeDriver from system PATH, or use webdriver manager
try:
    # First try with chromedriver.exe if it's in PATH
    service = Service('chromedriver.exe')
    browser = webdriver.Chrome(service=service, options=chrome_options)
except:
    try:
        # Alternative: let Selenium find ChromeDriver automatically
        browser = webdriver.Chrome(options=chrome_options)
    except:
        # Last resort: use full path
        service = Service(r'C:\ChromeDriver\chromedriver.exe')
        browser = webdriver.Chrome(service=service, options=chrome_options)

# Create ActionChains object
actions = ActionChains(browser)

def random_delay(min_delay=0.2, max_delay=0.5):
    """Random delay between actions to simulate human behavior."""
    time.sleep(random.uniform(min_delay, max_delay))

def reading_pause(min_delay=0.8, max_delay=1.5):
    """Longer pause to simulate reading field labels with idle mouse movements."""
    print("Reading field label...")
    pause_time = random.uniform(min_delay, max_delay)
    
    # Add some idle mouse movements during reading
    movements = random.randint(3, 7)
    movement_time = pause_time / movements
    
    for _ in range(movements):
        # Small random movements while "reading"
        idle_x = random.randint(-15, 15)
        idle_y = random.randint(-10, 10)
        
        try:
            actions.move_by_offset(idle_x, idle_y).perform()
        except:
            pass  # Ignore if movement fails
            
        time.sleep(movement_time * random.uniform(0.7, 1.3))
    
    # Final pause
    time.sleep(pause_time * 0.2)

def improved_mouse_movement(element, duration=0.3):
    """Enhanced mouse movement with realistic human-like patterns."""
    try:
        # Get element position for more natural movement
        element_rect = browser.execute_script("""
            var rect = arguments[0].getBoundingClientRect();
            return {x: rect.left, y: rect.top, width: rect.width, height: rect.height};
        """, element)
        
        # Calculate target position with some randomness
        target_x = element_rect['x'] + element_rect['width'] // 2 + random.randint(-5, 5)
        target_y = element_rect['y'] + element_rect['height'] // 2 + random.randint(-3, 3)
        
        # Generate more natural mouse movement with multiple intermediate points
        current_pos = browser.execute_script("return {x: window.mouseX || 100, y: window.mouseY || 100};")
        start_x = current_pos.get('x', 100)
        start_y = current_pos.get('y', 100)
        
        # Create curved path with 8-12 intermediate points
        num_points = random.randint(8, 12)
        for i in range(num_points):
            progress = (i + 1) / num_points
            
            # Add curve using sine wave for more natural movement
            curve_intensity = random.uniform(10, 25)
            curve_offset_x = math.sin(progress * math.pi) * curve_intensity * random.choice([-1, 1])
            curve_offset_y = math.sin(progress * math.pi * 0.5) * curve_intensity * 0.5 * random.choice([-1, 1])
            
            # Calculate intermediate position
            intermediate_x = start_x + (target_x - start_x) * progress + curve_offset_x
            intermediate_y = start_y + (target_y - start_y) * progress + curve_offset_y
            
            # Move to intermediate position with JavaScript for smoother movement
            browser.execute_script(f"""
                var event = new MouseEvent('mousemove', {{
                    clientX: {intermediate_x},
                    clientY: {intermediate_y},
                    bubbles: true
                }});
                document.dispatchEvent(event);
                window.mouseX = {intermediate_x};
                window.mouseY = {intermediate_y};
            """)
            
            # Small delay between movements
            time.sleep(random.uniform(0.02, 0.08))
        
        # Final move to exact element position
        actions.move_to_element(element).perform()
        
        # Add some small tremor movements (human hand isn't perfectly steady)
        for _ in range(random.randint(2, 5)):
            x_tremor = random.randint(-2, 2)
            y_tremor = random.randint(-2, 2)
            actions.move_by_offset(x_tremor, y_tremor).perform()
            time.sleep(random.uniform(0.03, 0.1))
            
    except Exception as e:
        print(f"Enhanced movement failed, using fallback: {e}")
        # Fallback to simple movement
        actions.move_to_element(element).perform()
        time.sleep(random.uniform(0.1, 0.3))

def human_like_typing(element, text):
    """Type character by character with realistic delays and occasional mistakes."""
    element.clear()  # Clear the field first
    
    # Calculate typing speed (characters per minute)
    base_speed = random.uniform(180, 300)  # 180-300 CPM (3-5 CPS)
    
    typed_text = ""
    i = 0
    
    while i < len(text):
        char = text[i]
        
        # Simulate typing mistakes (5% chance)
        if random.random() < 0.05 and i > 0:
            # Type wrong character
            wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
            element.send_keys(wrong_char)
            typed_text += wrong_char
            print(f"Typed (mistake): '{wrong_char}'")
            
            # Pause to "notice" mistake
            time.sleep(random.uniform(0.3, 0.8))
            
            # Backspace to correct
            element.send_keys(Keys.BACKSPACE)
            typed_text = typed_text[:-1]
            print("Corrected mistake (backspace)")
            time.sleep(random.uniform(0.1, 0.3))
        
        # Type the correct character
        element.send_keys(char)
        typed_text += char
        print(f"Typed: '{char}' (progress: {typed_text})")
        
        # Calculate delay based on character type
        if char.isdigit():
            # Numbers are slower to type
            delay = random.uniform(60/base_speed * 1.5, 60/base_speed * 2.0)
        elif char.isalpha():
            # Letters are normal speed
            delay = random.uniform(60/base_speed * 0.8, 60/base_speed * 1.2)
        else:
            # Special characters are slower
            delay = random.uniform(60/base_speed * 1.2, 60/base_speed * 1.8)
        
        # Add random variation
        delay *= random.uniform(0.7, 1.3)
        
        # Longer pause at word boundaries
        if char == ' ' or (i > 0 and text[i-1] == ' '):
            delay *= random.uniform(1.5, 2.5)
        
        time.sleep(delay)
        i += 1
    
    # Trigger input event for React
    browser.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
    print(f"Finished typing: '{text}'")

try:
    # Open the form page
    browser.get('http://localhost:3000/register')
    print("Opened form page, starting to fill...")

    # Wait for page to load
    time.sleep(random.uniform(2, 4))
    
    # Add initial page exploration movements (like a human scanning the page)
    print("Initial page exploration...")
    for _ in range(random.randint(5, 10)):
        explore_x = random.randint(-50, 50)
        explore_y = random.randint(-30, 30)
        try:
            actions.move_by_offset(explore_x, explore_y).perform()
            time.sleep(random.uniform(0.1, 0.4))
        except:
            pass
    
    # Simulate scrolling to see the full form
    browser.execute_script("window.scrollBy(0, 100);")
    time.sleep(random.uniform(0.5, 1.0))
    browser.execute_script("window.scrollBy(0, -50);")
    time.sleep(random.uniform(0.3, 0.8))

    # Function to safely locate an element and retry if it goes stale
    def get_element(by, value):
        for _ in range(3):
            try:
                return browser.find_element(by, value)
            except:
                time.sleep(0.5)
        raise Exception(f"Element with {by}='{value}' not found")

    # Form Fields with improved human-like behavior
    print("\n=== Starting Form Fill Process ===")
    
    # Name field
    print("\n1. Filling Name field...")
    name_input = get_element(By.ID, 'name')
    reading_pause()  # Read the label
    improved_mouse_movement(name_input)
    random_delay(0.3, 0.7)
    human_like_typing(name_input, 'John Smith')
    random_delay(0.5, 1.0)

    # Email field
    print("\n2. Filling Email field...")
    email_input = get_element(By.ID, 'email')
    reading_pause()  # Read the label
    improved_mouse_movement(email_input)
    random_delay(0.3, 0.7)
    human_like_typing(email_input, 'john.smith@email.com')
    random_delay(0.5, 1.0)

    # Father's name field
    print("\n3. Filling Father's Name field...")
    fathers_name_input = get_element(By.ID, 'fathers_name')
    reading_pause()  # Read the label
    improved_mouse_movement(fathers_name_input)
    random_delay(0.3, 0.7)
    human_like_typing(fathers_name_input, 'Robert Smith')
    random_delay(0.5, 1.0)

    # Aadhaar field (slower for numbers)
    print("\n4. Filling Aadhaar field...")
    aadhaar_input = get_element(By.ID, 'aadhaar')
    reading_pause(1.2, 2.0)  # Longer pause for complex field
    improved_mouse_movement(aadhaar_input)
    random_delay(0.4, 0.8)
    human_like_typing(aadhaar_input, '12345678901234')
    random_delay(0.7, 1.2)

    # EID field (slower for numbers)
    print("\n5. Filling EID field...")
    eid_input = get_element(By.ID, 'eid')
    reading_pause(1.0, 1.8)  # Longer pause for complex field
    improved_mouse_movement(eid_input)
    random_delay(0.4, 0.8)
    human_like_typing(eid_input, '123456789012')
    random_delay(0.7, 1.2)

    # Phone field
    print("\n6. Filling Phone field...")
    phone_input = get_element(By.ID, 'phone')
    reading_pause()  # Read the label
    improved_mouse_movement(phone_input)
    random_delay(0.3, 0.7)
    human_like_typing(phone_input, '9876543210')
    random_delay(0.5, 1.0)

    # HONEYPOT TRIGGERS: Improved bot should trigger 2 honeypots
    print("\n🍯 Improved bot triggering honeypots: Hidden field + JS optional field")
    
    # Trigger 1: Hidden CSS field (bots see all fields)
    try:
        hidden_field = get_element(By.ID, 'website_url')
        improved_mouse_movement(hidden_field)
        human_like_typing(hidden_field, 'http://automated-bot.com')
        print("✅ Hidden honeypot field filled successfully")
        random_delay(0.3, 0.6)
    except Exception as e:
        print(f"⚠️ Could not trigger hidden honeypot: {e}")
    
    # Trigger 2: JS optional field (make it visible first, then fill)
    try:
        # Show the JS optional field (simulate JS being disabled or bot behavior)
        browser.execute_script("""
            var jsField = document.getElementById('js-optional-container');
            if (jsField) {
                jsField.style.display = 'block';
                jsField.style.visibility = 'visible';
            }
        """)
        time.sleep(random.uniform(0.2, 0.5))
        
        optional_field = get_element(By.ID, 'optional_info')
        improved_mouse_movement(optional_field)
        human_like_typing(optional_field, 'Extra bot information')
        print("✅ JS optional honeypot field filled successfully")
        random_delay(0.3, 0.6)
    except Exception as e:
        print(f"⚠️ Could not trigger JS optional honeypot: {e}")

    # Brief form review pause
    print("\n7. Reviewing filled form...")
    time.sleep(random.uniform(2, 4))

    # Submit button
    print("\n8. Submitting form...")
    submit_button = get_element(By.XPATH, '//button[@type="submit"]')
    
    # Pause before submission (hesitation)
    reading_pause(1.5, 2.5)
    improved_mouse_movement(submit_button)
    
    # Hover over submit button briefly
    time.sleep(random.uniform(0.5, 1.0))
    
    # Verify all fields are filled
    print("Verifying form fields are completed...")
    print(f"Name: {name_input.get_attribute('value')}")
    print(f"Email: {email_input.get_attribute('value')}")
    print(f"Aadhaar: {aadhaar_input.get_attribute('value')}")
    print(f"EID: {eid_input.get_attribute('value')}")
    print(f"Father's Name: {fathers_name_input.get_attribute('value')}")
    print(f"Phone: {phone_input.get_attribute('value')}")
    
    # Submit the form
    submit_clicked = False
    try:
        submit_button.click()
        print("Submit button clicked successfully!")
        submit_clicked = True
    except Exception as e:
        print(f"Standard click failed: {e}")
        try:
            browser.execute_script("arguments[0].click();", submit_button)
            print("JavaScript click succeeded!")
            submit_clicked = True
        except Exception as e2:
            print(f"JavaScript click failed: {e2}")
            try:
                actions.move_to_element(submit_button).click().perform()
                print("ActionChains click succeeded!")
                submit_clicked = True
            except Exception as e3:
                print(f"ActionChains click failed: {e3}")

    if not submit_clicked:
        print("ERROR: Could not click submit button!")
    else:
        print("Form submitted successfully!")

    # Wait to see the result
    print("\nWaiting for submission result...")
    time.sleep(5)
    
    # Check current URL and results
    current_url = browser.current_url
    print(f"Current URL after submission: {current_url}")
    
    # Check for success indicators
    try:
        toast = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast--success')
        if toast:
            print("SUCCESS: Form submitted successfully (success toast found)")
            print("Result: HUMAN BEHAVIOR DETECTED")
    except:
        try:
            if '/verify' in current_url:
                print("BOT DETECTED: Redirected to verification page")
                print("Result: BOT BEHAVIOR DETECTED")
            else:
                print("UNKNOWN: No clear success indicator found")
        except:
            print("Could not determine submission result")

    # Wait for user input before closing
    input("\nPress Enter to close the browser...")

finally:
    # Close the browser
    browser.quit()
    print("Browser closed. Bot session complete.")
