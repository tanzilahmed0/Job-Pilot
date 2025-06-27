from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def open_application_page(job_url: str):
    """
    Launches a browser and navigates to the specified job application URL.

    Args:
        job_url: The URL of the job page to open.
    """
    if not job_url:
        print("Error: No job URL provided.")
        return

    options = Options()
    # The "detach" option keeps the browser open after the script finishes
    options.add_experimental_option("detach", True)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"Opening job application page: {job_url}")
        driver.get(job_url)
        # The browser will remain open for you to inspect.
        # You can manually close it when you're done.
        print("Browser has been opened. Please inspect the page.")
        # We'll wait here in the script just to keep it running for a moment.
        time.sleep(10)
    except Exception as e:
        print(f"An error occurred: {e}")
        # The browser will close automatically if an error occurs before detach is effective
        driver.quit()


if __name__ == '__main__':
    # --- Test Case ---
    # This is a sample URL. In the real flow, this will come from the scraper.
    # Note: This link might expire. If it fails, you can replace it with any
    # valid LinkedIn job posting URL for testing purposes.
    test_url = "https://www.linkedin.com/jobs/view/3962294336"
    
    print("--- Testing open_application_page() ---")
    open_application_page(test_url)
    print("Test finished. If a browser window opened, the test was successful.")
