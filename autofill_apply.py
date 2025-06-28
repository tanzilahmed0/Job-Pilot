from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

def open_application_page(job_url: str):
    """
    Launches a browser, logs into LinkedIn, and navigates to the job page.

    Args:
        job_url: The URL of the job page to open.
    """
    if not job_url:
        print("Error: No job URL provided.")
        return
        
    linkedin_username = os.getenv("LINKEDIN_USERNAME")
    linkedin_password = os.getenv("LINKEDIN_PASSWORD")

    if not linkedin_username or not linkedin_password:
        print("Error: LinkedIn credentials not found in .env file.")
        return

    options = Options()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Step 1: Log in to LinkedIn
        print("Navigating to LinkedIn login page...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        print("Entering credentials...")
        driver.find_element(By.ID, "username").send_keys(linkedin_username)
        driver.find_element(By.ID, "password").send_keys(linkedin_password)
        
        print("Signing in...")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Wait for the login to complete and the page to load
        time.sleep(5) 
        
        # Step 2: Navigate to the job application page
        print(f"Login successful. Navigating to job page: {job_url}")
        driver.get(job_url)

        print("Browser has been opened. Please inspect the page.")
        # Keep the script running to allow inspection
        time.sleep(10)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # The browser will be detached, so we don't call quit() here.
        # This allows the user to inspect or take over the session.
        print("Script finished. The browser window will remain open.")

if __name__ == '__main__':
    # --- Test Case ---
    # Replace this with a valid, active LinkedIn job URL.
    test_url = "https://www.linkedin.com/jobs/view/3962294336" # This might be expired
    
    print("--- Testing open_application_page() ---")
    open_application_page(test_url)
    print("Test finished. If the browser logged in and went to the job page, the test was successful.")
