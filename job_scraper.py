from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

def scrape_job_listings():
    """
    Opens the job board, scrapes job listings (title, company, link),
    visits each link to get the full description,
    and returns them as a list of dictionaries.
    """
    job_board_url = os.getenv("JOB_BOARD_URL")
    if not job_board_url:
        print("Error: JOB_BOARD_URL not found in .env file.")
        return []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    job_cards_with_descriptions = []

    try:
        # Step 1: Get basic job info from the search results page
        print(f"Navigating to {job_board_url}...")
        driver.get(job_board_url)
        time.sleep(10) 
        print("Page loaded. Scraping initial job cards...")

        job_list_container = driver.find_element(By.CSS_SELECTOR, ".jobs-search__results-list")
        jobs_elements = job_list_container.find_elements(By.TAG_NAME, "li")
        
        initial_job_cards = []
        for job_element in jobs_elements:
            try:
                title = job_element.find_element(By.CSS_SELECTOR, '.base-search-card__title').text
                company = job_element.find_element(By.CSS_SELECTOR, '.base-search-card__subtitle').text
                link = job_element.find_element(By.CSS_SELECTOR, '.base-card__full-link').get_attribute('href')
                
                if title and company and link:
                    initial_job_cards.append({
                        "title": title,
                        "company": company,
                        "link": link
                    })
            except NoSuchElementException:
                continue
        
        print(f"Found {len(initial_job_cards)} initial job listings.")

        # Step 2: Visit each job link to scrape the full description
        for job in initial_job_cards:
            try:
                print(f"Scraping description for: {job['title']}...")
                driver.get(job['link'])
                time.sleep(3)

                # Click the "See more" button to expand the description
                try:
                    see_more_button = driver.find_element(By.CSS_SELECTOR, '.show-more-less-html__button--more')
                    driver.execute_script("arguments[0].click();", see_more_button)
                    time.sleep(1)
                except NoSuchElementException:
                    pass # No button found, proceed

                description_container = driver.find_element(By.CSS_SELECTOR, ".description__text")
                job['description'] = description_container.get_attribute('innerText')
                job_cards_with_descriptions.append(job)

            except Exception as e:
                print(f"  - Could not scrape description for {job['title']}. Error: {e}")
                continue
        
        print(f"Successfully scraped descriptions for {len(job_cards_with_descriptions)} jobs.")
        return job_cards_with_descriptions
    finally:
        print("Closing browser.")
        driver.quit()


if __name__ == '__main__':
    jobs = scrape_job_listings()
    if jobs:
        print("\n--- Scraped Jobs with Descriptions ---")
        for job in jobs:
            print(f"Title: {job['title']}, Company: {job['company']}")
            description_preview = job.get('description', 'N/A').strip().replace('\n', ' ')
            print(f"  Description: {description_preview[:100]}...")
        print(f"\nSuccessfully scraped {len(jobs)} jobs with descriptions.")
