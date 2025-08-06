import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

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
    """Reduced random delay between actions to simulate human behavior."""
    time.sleep(random.uniform(min_delay, max_delay))

def random_mouse_movement(element, duration=0.5):
    """Move mouse in a random pattern over an element for a shorter duration."""
    actions.move_to_element(element).perform()
    for _ in range(int(duration * 10)):  # Reduced movement time
        x_offset = random.randint(-5, 5)
        y_offset = random.randint(-5, 5)
        actions.move_by_offset(x_offset, y_offset).perform()
        random_delay(0.05, 0.1)  # Reduced micro-delays for quicker movements

try:
    # Open the form page
    browser.get('http://localhost:3000/register')  # Replace with your actual local URL

    # Function to safely locate an element and retry if it goes stale
    def get_element(by, value):
        for _ in range(3):  # Retry up to 3 times if a stale element reference occurs
            try:
                return browser.find_element(by, value)
            except:
                time.sleep(0.5)  # Shorter wait for the DOM to stabilize before retrying
        raise Exception(f"Element with {by}='{value}' not found")

    # Form Fields
    name_input = get_element(By.ID, 'name')
    email_input = get_element(By.ID, 'email')
    aadhaar_input = get_element(By.ID, 'aadhaar')
    eid_input = get_element(By.ID, 'eid')
    fathers_name_input = get_element(By.ID, 'fathers_name')
    phone_input = get_element(By.ID, 'phone')
    submit_button = get_element(By.XPATH, '//button[@type="submit"]')
    
    # HONEYPOT TRIGGER: Simple bot should trigger the hidden CSS field
    # This simulates a basic bot that fills all visible fields including hidden ones
    print("🍯 Simple bot triggering honeypot: Hidden CSS field")
    try:
        hidden_field = get_element(By.ID, 'website_url')
        hidden_field.send_keys('http://bot-detected.com')
        print("✅ Hidden honeypot field filled successfully")
    except Exception as e:
        print(f"⚠️ Could not trigger hidden honeypot: {e}")

    # Fill in the form fields
    random_mouse_movement(name_input)
    name_input.send_keys('Bot Name')
    browser.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", name_input)
    random_delay(0.2, 0.5)

    random_mouse_movement(email_input)
    email_input.send_keys('bot@example.com')
    browser.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", email_input)
    random_delay(0.2, 0.5)

    random_mouse_movement(aadhaar_input)
    aadhaar_input.send_keys('12345678901234')
    browser.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", aadhaar_input)
    random_delay(0.2, 0.5)

    random_mouse_movement(eid_input)
    eid_input.send_keys('123456789012')
    browser.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", eid_input)
    random_delay(0.2, 0.5)

    random_mouse_movement(fathers_name_input)
    fathers_name_input.send_keys('Bot Father')
    browser.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", fathers_name_input)
    random_delay(0.2, 0.5)

    random_mouse_movement(phone_input)
    phone_input.send_keys('9876543210')
    browser.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", phone_input)
    random_delay(0.2, 0.5)

    # Wait for form to be fully loaded
    time.sleep(2)
    
    # Move over the submit button and try multiple click methods
    print("Attempting to click submit button...")
    random_mouse_movement(submit_button)
    random_delay(0.3, 0.6)
    
    # Ensure all fields are properly filled before submission
    print("Verifying form fields are filled...")
    print(f"Name: {name_input.get_attribute('value')}")
    print(f"Email: {email_input.get_attribute('value')}")
    print(f"Aadhaar: {aadhaar_input.get_attribute('value')}")
    print(f"EID: {eid_input.get_attribute('value')}")
    print(f"Father's Name: {fathers_name_input.get_attribute('value')}")
    print(f"Phone: {phone_input.get_attribute('value')}")
    
    # Try multiple approaches to click the submit button
    submit_clicked = False
    try:
        # Method 1: Standard click
        submit_button.click()
        print("Submit button clicked successfully!")
        submit_clicked = True
    except Exception as e:
        print(f"Standard click failed: {e}")
        try:
            # Method 2: JavaScript click
            browser.execute_script("arguments[0].click();", submit_button)
            print("JavaScript click succeeded!")
            submit_clicked = True
        except Exception as e2:
            print(f"JavaScript click failed: {e2}")
            try:
                # Method 3: ActionChains click
                actions.move_to_element(submit_button).click().perform()
                print("ActionChains click succeeded!")
                submit_clicked = True
            except Exception as e3:
                print(f"ActionChains click failed: {e3}")
                # Method 4: Form submission via JavaScript
                try:
                    browser.execute_script("document.querySelector('form').submit();")
                    print("Form JavaScript submit succeeded!")
                    submit_clicked = True
                except Exception as e4:
                    print(f"Form submit failed: {e4}")

    if not submit_clicked:
        print("ERROR: Could not click submit button!")
    else:
        print("Submit button was clicked successfully!")

    # Wait to see the result and check if form was submitted
    print("Waiting to see form submission result...")
    time.sleep(5)
    
    # Check current URL to see if redirected
    current_url = browser.current_url
    print(f"Current URL after submission: {current_url}")
    
    # Check if there are any toasts or popups
    try:
        # Look for success toast
        toast = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast--success')
        if toast:
            print("SUCCESS: Form submitted successfully (success toast found)")
    except:
        try:
            # Check if redirected to verify page
            if '/verify' in current_url:
                print("BOT DETECTED: Redirected to verification page")
            else:
                print("UNKNOWN: No clear success indicator found")
        except:
            print("Could not determine submission result")

    # Wait for user input before closing
    input("Press Enter to close the browser...")

finally:
    # Close the browser
    browser.quit()
