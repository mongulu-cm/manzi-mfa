from typing import List

from models.job import Job
from scrapers.base_scraper import JobScraper
from utils.selenium import scroll_and_extract_jobs
from utils.selenium import setup_chrome_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

class ScrollScraper(JobScraper):
    def __init__(self, url: str, driver_path: str):
        self.url = url
        self.driver_path = driver_path

    def scrape(self) -> List[Job]:
        driver = setup_chrome_driver(self.driver_path)
        all_jobs = []
        screenshots = []

        try:
            driver.get(self.url)
            time.sleep(2)

            # Gestion des cookies
            try:
                cookie_decline_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonDecline"))
                )
                cookie_decline_button.click()
            except:
                print("Cookie decline button not found or not clickable.")

            scroll_and_extract_jobs(driver, all_jobs, screenshots)

        finally:
            driver.quit()
            # Nettoyage des fichiers temporaires
            for path in screenshots:
                os.remove(path)

        return all_jobs