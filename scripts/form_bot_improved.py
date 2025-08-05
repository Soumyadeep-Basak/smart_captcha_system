import random
import time
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
    """Longer pause to simulate reading field labels."""
    print("Reading field label...")
    time.sleep(random.uniform(min_delay, max_delay))

def improved_mouse_movement(element, duration=0.3):
    """Slightly improved mouse movement with some randomness."""
    # Move to element with small random offset
    actions.move_to_element(element).perform()
    
    # Add some small random movements
    for _ in range(random.randint(2, 4)):
        x_offset = random.randint(-3, 3)
        y_offset = random.randint(-3, 3)
        actions.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.05, 0.15))

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

    # Function to safely locate an element and retry if it goes stale
    def get_element(by, value):
        for _ in range(3):
            try:
                return browser.find_element(by, value)
            except:
                time.sleep(0.5)
        raise Exception(f"Element with {by}='{value}' not found")

    # Wait for page to load
    time.sleep(random.uniform(2, 4))

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
