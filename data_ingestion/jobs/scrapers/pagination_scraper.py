from typing import List

from tqdm import tqdm
from scrapers.base_scraper import JobScraper
from utils.selenium import scroll_and_extract_jobs
from utils.selenium import setup_chrome_driver
from selenium.webdriver.common.action_chains import ActionChains
from models.job import Job
import time
import os

class PaginationScraper(JobScraper):
    def __init__(self, url: str, driver_path: str, next_button_x: int, next_button_y: int, cookie_x: int = None, cookie_y: int = None):
        self.url = url
        self.driver_path = driver_path
        self.next_button_x = next_button_x
        self.next_button_y = next_button_y
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

            last_page_content = ""
            page_count = 0

            while True:

                # Vérifier si on est à la dernière page
                current_page_content = driver.page_source
                if current_page_content == last_page_content:
                    print("Contenu de page identique détecté - Fin de la pagination atteinte")
                    break

                scroll_and_extract_jobs(driver, all_jobs, screenshots)


                last_page_content = current_page_content

                # Préparation du clic sur le bouton suivant
                viewport_height = driver.execute_script("return window.innerHeight")
                scroll_position = (self.next_button_y // viewport_height) * viewport_height

                # Scroll jusqu'au bouton
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(0.5)

                # Clic sur le bouton suivant
                actions = ActionChains(driver)
                relative_y = self.next_button_y % viewport_height
                actions.move_by_offset(self.next_button_x, relative_y).click().perform()

                page_count += 1
                print(f"Page {page_count} traitée")

                # Réinitialiser la position du curseur
                actions.move_by_offset(-self.next_button_x, -relative_y).perform()

                time.sleep(10)  # Attendre le chargement de la nouvelle page

        except Exception as e:
            print(f"Erreur lors du scraping : {e}")
        finally:
            driver.quit()
            # Nettoyage des fichiers temporaires
            for path in screenshots:
                os.remove(path)


        return all_jobs