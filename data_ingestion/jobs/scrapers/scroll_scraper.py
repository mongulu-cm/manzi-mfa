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
    def __init__(self, url: str, driver_path: str, cookie_x: int = None, cookie_y: int = None):
        self.url = url
        self.driver_path = driver_path
        self.cookie_x = cookie_x
        self.cookie_y = cookie_y

    def scrape(self) -> List[Job]:
        driver = setup_chrome_driver(self.driver_path)
        all_jobs = []
        screenshots = []

        try:
            driver.get(self.url)
            time.sleep(2)

            if self.cookie_x is not None and self.cookie_y is not None:
                from selenium.webdriver import ActionChains
                ActionChains(driver).move_by_offset(self.cookie_x, self.cookie_y).click().perform()
            else:
                print("Cookie x,y not provided, skipping cookie click.")

            scroll_and_extract_jobs(driver, all_jobs, screenshots)

        finally:
            driver.quit()
            # Nettoyage des fichiers temporaires
            for path in screenshots:
                os.remove(path)

        return all_jobs