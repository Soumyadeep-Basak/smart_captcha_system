import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Set up the WebDriver options
chrome_options = Options()
chrome_options.add_argument("-incognito")
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

# Path to the ChromeDriver executable
service = Service(executable_path=r'C:\Users\Harsh\Downloads\chromedriver.exe')

# Initialize the WebDriver
browser = webdriver.Chrome(service=service, options=chrome_options)

# Create ActionChains object
actions = ActionChains(browser)

def random_delay(min_delay=1, max_delay=3):
    """Random delay between actions to simulate human behavior."""
    time.sleep(random.uniform(min_delay, max_delay))

def random_mouse_movement(element, duration=1):
    """Move mouse in a random pattern over an element for a given duration."""
    actions.move_to_element(element).perform()
    for _ in range(int(duration * 10)):  # Simulate movement for 'duration' seconds
        x_offset = random.randint(-10, 10)
        y_offset = random.randint(-10, 10)
        actions.move_by_offset(x_offset, y_offset).perform()
        random_delay(0.1, 0.3)
    print(f"Mouse moved over {element.get_attribute('id')}")

try:
    # Open the form page
    browser.get('http://localhost:3000/register')  # Replace with your actual local URL

    # Function to safely locate an element and retry if it goes stale
    def get_element(by, value):
        for _ in range(3):  # Retry up to 3 times if a stale element reference occurs
            try:
                return browser.find_element(by, value)
            except:
                time.sleep(1)  # Wait for the DOM to stabilize before retrying
        raise Exception(f"Element with {by}='{value}' not found")

    # Form Fields
    name_input = get_element(By.ID, 'name')
    email_input = get_element(By.ID, 'email')
    aadhaar_input = get_element(By.ID, 'aadhaar')
    eid_input = get_element(By.ID, 'eid')
    fathers_name_input = get_element(By.ID, 'fathers_name')
    phone_input = get_element(By.ID, 'phone')
    message_input = get_element(By.ID, 'message')
    submit_button = get_element(By.XPATH, '//button[@type="submit"]')

    # Move the mouse over all fields multiple times before filling
    for _ in range(2):  # Move over all fields twice
        random_mouse_movement(name_input)
        random_mouse_movement(email_input)
        random_mouse_movement(aadhaar_input)
        random_mouse_movement(eid_input)
        random_mouse_movement(fathers_name_input)
        random_mouse_movement(phone_input)
        random_mouse_movement(message_input)
        random_delay(1, 2)  # Wait before another round
    print("Bot is filling the form...")

    # Fill in the form fields with random delay
    random_mouse_movement(name_input)
    name_input.send_keys('Bot Name')
    random_delay(0.5, 1.5)

    random_mouse_movement(email_input)
    email_input.send_keys('bot@example.com')
    random_delay(0.5, 1.5)

    random_mouse_movement(aadhaar_input)
    aadhaar_input.send_keys('12345678901234')
    random_delay(0.5, 1.5)

    random_mouse_movement(eid_input)
    eid_input.send_keys('123456789012')
    random_delay(0.5, 1.5)

    random_mouse_movement(fathers_name_input)
    fathers_name_input.send_keys('Bot Father')
    random_delay(0.5, 1.5)

    random_mouse_movement(phone_input)
    phone_input.send_keys('9876543210')
    random_delay(0.5, 1.5)

    random_mouse_movement(message_input)
    message_input.send_keys('This is a message from the bot.')
    random_delay(0.5, 1.5)

    # Move over the submit button two times before clicking
    for _ in range(2):
        random_mouse_movement(submit_button)
        random_delay(0.5, 1)
    
    # driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

    # Click the submit button
    random_mouse_movement(submit_button, duration=0.5)
    submit_button.click()

    # Wait to ensure the form submission is processed
    # time.sleep(5)

    # Move the mouse to the CSV download button and click it
    # download_button = get_element(By.ID, 'download-csv')
    # random_mouse_movement(download_button, duration=0.5)
    # download_button.click()

    # Wait to ensure the CSV file is downloaded
    time.sleep(10)  # Adjust this time if needed

finally:
    # Close the browser
    browser.quit()