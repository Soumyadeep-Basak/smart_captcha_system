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

# Path to the ChromeDriver executable
service = Service(executable_path=r'C:\Users\yaahg\chromedriver.exe')

# Initialize the WebDriver
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

    # Move over the submit button
    random_mouse_movement(submit_button)
    random_delay(0.3, 0.6)
    
    # Click the submit button
    random_mouse_movement(submit_button, duration=0.3)
    submit_button.click()

    # Wait to ensure the form submission is processed
    time.sleep(3)

finally:
    # Close the browser
    browser.quit()
