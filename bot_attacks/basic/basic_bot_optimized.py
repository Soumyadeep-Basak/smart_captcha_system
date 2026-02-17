import random
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Advanced Chrome options to appear more human-like
chrome_options = Options()
chrome_options.add_argument("-incognito")
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')

# Use webdriver-manager for automatic ChromeDriver version management
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# Remove webdriver property to evade detection
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    '''
})

actions = ActionChains(browser)

def human_like_delay(min_sec=0.1, max_sec=0.5):
    """Random delay to simulate human behavior"""
    time.sleep(random.uniform(min_sec, max_sec))

def human_like_typing(element, text):
    """Type like a human with random delays between keystrokes"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # Random delay between 50-200ms

def human_like_mouse_movement(browser, element):
    """Simulate human-like mouse movement to an element"""
    # Get element location
    location = element.location
    size = element.size
    
    # Target center of element with slight randomness
    target_x = location['x'] + size['width'] / 2 + random.randint(-5, 5)
    target_y = location['y'] + size['height'] / 2 + random.randint(-5, 5)
    
    # Perform smooth movement with curves
    actions = ActionChains(browser)
    actions.move_to_element_with_offset(element, random.randint(-2, 2), random.randint(-2, 2))
    actions.pause(random.uniform(0.1, 0.3))
    actions.perform()

def scroll_smoothly(browser, amount=300):
    """Scroll page smoothly like a human"""
    current_position = browser.execute_script("return window.pageYOffset;")
    target_position = current_position + amount
    step = 10
    
    while current_position < target_position:
        current_position += step
        browser.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(random.uniform(0.01, 0.03))

try:
    print("[+] Starting optimized bot attack...")
    browser.get('http://localhost:3000/register')
    
    # Wait for page to load with random human-like delay
    human_like_delay(2, 4)
    
    # Simulate reading the page
    print("[+] Simulating page reading behavior...")
    scroll_smoothly(browser, 100)
    human_like_delay(1, 2)
    scroll_smoothly(browser, -50)
    human_like_delay(0.5, 1)

    def get_element(by, value):
        for _ in range(3):
            try:
                return browser.find_element(by, value)
            except:
                time.sleep(1)
        raise Exception(f"Element with {by}='{value}' not found")

    # Locate all form fields
    print("[+] Locating form fields...")
    name_input = get_element(By.ID, 'name')
    email_input = get_element(By.ID, 'email')
    aadhaar_input = get_element(By.ID, 'aadhaar')
    eid_input = get_element(By.ID, 'eid')
    fathers_name_input = get_element(By.ID, 'fathers_name')
    phone_input = get_element(By.ID, 'phone')
    submit_button = get_element(By.XPATH, '//button[@type="submit"]')

    # Fill form with human-like behavior
    print("[+] Filling form with human-like behavior...")
    
    # Name field
    human_like_mouse_movement(browser, name_input)
    name_input.click()
    human_like_delay(0.3, 0.7)
    human_like_typing(name_input, 'John Doe')
    human_like_delay(0.5, 1)
    
    # Email field
    human_like_mouse_movement(browser, email_input)
    email_input.click()
    human_like_delay(0.3, 0.7)
    human_like_typing(email_input, 'john.doe@example.com')
    human_like_delay(0.5, 1)
    
    # Aadhaar field
    human_like_mouse_movement(browser, aadhaar_input)
    aadhaar_input.click()
    human_like_delay(0.3, 0.7)
    human_like_typing(aadhaar_input, '123456789012')
    human_like_delay(0.5, 1)
    
    # EID field
    human_like_mouse_movement(browser, eid_input)
    eid_input.click()
    human_like_delay(0.3, 0.7)
    human_like_typing(eid_input, '987654321098')
    human_like_delay(0.5, 1)
    
    # Father's name field
    human_like_mouse_movement(browser, fathers_name_input)
    fathers_name_input.click()
    human_like_delay(0.3, 0.7)
    human_like_typing(fathers_name_input, 'Robert Doe')
    human_like_delay(0.5, 1)
    
    # Phone field
    human_like_mouse_movement(browser, phone_input)
    phone_input.click()
    human_like_delay(0.3, 0.7)
    human_like_typing(phone_input, '9876543210')
    human_like_delay(1, 2)
    
    # Simulate reviewing the form
    print("[+] Simulating form review...")
    scroll_smoothly(browser, -200)
    human_like_delay(1, 2)
    scroll_smoothly(browser, 200)
    human_like_delay(0.5, 1)
    
    # Submit the form
    print("[+] Attempting to submit form...")
    human_like_mouse_movement(browser, submit_button)
    human_like_delay(0.5, 1)
    
    try:
        submit_button.click()
        print("[✓] Submit button clicked successfully!")
    except Exception as e:
        print(f"[!] Standard click failed: {e}")
        try:
            browser.execute_script("arguments[0].click();", submit_button)
            print("[✓] JavaScript click succeeded!")
        except Exception as e2:
            print(f"[✗] JavaScript click also failed: {e2}")

    # Wait to see the result
    print("[+] Waiting for submission result...")
    time.sleep(5)
    
    # Check current URL and results
    current_url = browser.current_url
    print(f"\n[*] Current URL: {current_url}")
    
    # Check for success indicators
    try:
        toast = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast--success')
        if toast:
            print("\n[✓] SUCCESS: Form submitted successfully (success toast found)")
            print("[!] Bot bypassed the detection system!")
    except:
        try:
            if '/verify' in current_url:
                print("\n[✗] BOT DETECTED: Redirected to verification page")
                print("[!] The system detected bot behavior")
            else:
                print("\n[?] UNKNOWN: No clear success indicator found")
        except:
            print("\n[?] Could not determine submission result")

    # Keep browser open for inspection
    print("\n[+] Press Enter to close the browser...")
    input()
    
except Exception as e:
    print(f"\n[✗] Error occurred: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to close...")
    
finally:
    print("\n[+] Closing browser...")
    browser.quit()
    print("[+] Bot execution completed.")