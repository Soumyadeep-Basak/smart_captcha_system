import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_argument("-incognito")
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

# Try to use ChromeDriver from system PATH, or use webdriver manager
try:
    # First try with just 'chromedriver' if it's in PATH
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

actions = ActionChains(browser)




try:
    browser.get('http://localhost:3000/register') 

    def get_element(by, value):
        for _ in range(3): 
            try:
                return browser.find_element(by, value)
            except:
                time.sleep(1)  
        raise Exception(f"Element with {by}='{value}' not found")

    # Form Fields
    name_input = get_element(By.ID, 'name')
    email_input = get_element(By.ID, 'email')
    aadhaar_input = get_element(By.ID, 'aadhaar')
    eid_input = get_element(By.ID, 'eid')
    fathers_name_input = get_element(By.ID, 'fathers_name')
    phone_input = get_element(By.ID, 'phone')
    submit_button = get_element(By.XPATH, '//button[@type="submit"]')

    name_input.send_keys('Bot Name')

    email_input.send_keys('bot@example.com')
    
    aadhaar_input.send_keys('12345678901234')
    
    eid_input.send_keys('123456789012')
    
    fathers_name_input.send_keys('Bot Father')
    
    phone_input.send_keys('9876543210')
    
    # Try multiple click methods for submit button
    try:
        submit_button.click()
        print("Submit button clicked successfully!")
    except Exception as e:
        print(f"Standard click failed: {e}")
        try:
            browser.execute_script("arguments[0].click();", submit_button)
            print("JavaScript click succeeded!")
        except Exception as e2:
            print(f"JavaScript click also failed: {e2}")

    # Wait to see the result
    print("Waiting to see form submission result...")
    time.sleep(5)
    
    # Check current URL and results
    current_url = browser.current_url
    print(f"Current URL after submission: {current_url}")
    
    # Check for success indicators
    try:
        toast = browser.find_element(By.CSS_SELECTOR, '.Toastify__toast--success')
        if toast:
            print("SUCCESS: Form submitted successfully (success toast found)")
    except:
        try:
            if '/verify' in current_url:
                print("BOT DETECTED: Redirected to verification page")
            else:
                print("UNKNOWN: No clear success indicator found")
        except:
            print("Could not determine submission result")

    input("Press Enter to close the browser...")
finally:
    print("Bot has completed the form submission.")