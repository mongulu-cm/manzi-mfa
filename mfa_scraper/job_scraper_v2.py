from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

class JobScraper:
    def __init__(self, driver_path, target_url):
        self.driver = webdriver.Chrome(driver_path)
        self.target_url = target_url

    def open_website(self):
        self.driver.get(self.target_url)
        time.sleep(3)  # Wait for the page to load

    def extract_job_data(self, job_card):
        try:
            title = job_card.find_element(By.CSS_SELECTOR, ".title").text
            company = job_card.find_element(By.CSS_SELECTOR, ".company").text
            location = job_card.find_element(By.CSS_SELECTOR, ".location").text
            description = job_card.find_element(By.CSS_SELECTOR, ".description").text
            return {
                "title": title,
                "company": company,
                "location": location,
                "description": description
            }
        except NoSuchElementException:
            return None

    def scrape_jobs(self):
        self.open_website()
        job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-card-selector")
        jobs = []

        for card in job_cards:
            job_data = self.extract_job_data(card)
            if job_data:
                jobs.append(job_data)
        return jobs

    def close_browser(self):
        self.driver.quit()

# Usage
driver_path = "path/to/your/chromedriver"  # Update this with your Chromedriver path
target_url = "https://www.example.com/jobs"  # Update this with the website you are targeting
scraper = JobScraper(driver_path, target_url)
job_listings = scraper.scrape_jobs()
scraper.close_browser()

for job in job_listings:
    print(job)
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

class JobScraper:
    def __init__(self, driver_path, target_url):
        self.driver = webdriver.Chrome(driver_path)
        self.target_url = target_url

    def open_website(self):
        self.driver.get(self.target_url)
        time.sleep(3)  # Wait for the page to load

    def extract_job_data(self, job_card):
        try:
            title = job_card.find_element(By.CSS_SELECTOR, ".title").text
            company = job_card.find_element(By.CSS_SELECTOR, ".company").text
            location = job_card.find_element(By.CSS_SELECTOR, ".location").text
            description = job_card.find_element(By.CSS_SELECTOR, ".description").text
            return {
                "title": title,
                "company": company,
                "location": location,
                "description": description
            }
        except NoSuchElementException:
            return None

    def scrape_jobs(self):
        self.open_website()
        job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-card-selector")
        jobs = []

        for card in job_cards:
            job_data = self.extract_job_data(card)
            if job_data:
                jobs.append(job_data)
        return jobs

    def close_browser(self):
        self.driver.quit()

# Usage
driver_path = "path/to/your/chromedriver"  # Update this with your Chromedriver path
target_url = "https://www.example.com/jobs"  # Update this with the website you are targeting
scraper = JobScraper(driver_path, target_url)
job_listings = scraper.scrape_jobs()
scraper.close_browser()

for job in job_listings:
    print(job)
