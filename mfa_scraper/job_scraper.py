from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
from datetime import datetime
import json

# set up a controllable Chrome instance
# in headless mode
service = Service()
options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
driver = webdriver.Chrome(
    service=service,
    options=options
)

# open the target page  in the browser
driver.get("https://www.indeed.com/jobs?q=data&l=&vjk=e90a1cb0b8b2d848")
# set the window size to make sure pages
# will not be rendered in responsive mode
driver.set_window_size(1920, 1080)

# a data structure where to store the job openings
# scraped from the page
jobs = []

pages_scraped = 0
pages_to_scrape = 1
while pages_scraped < pages_to_scrape:
    # select the job posting cards on the page
    job_cards = driver.find_elements(By.CSS_SELECTOR, ".cardOutline")

    for job_card in job_cards:
        # initialize a dictionary to store the scraped job data
        job = {}

        # initialize the job attributes to scrape
        posted_at = None
        applications = None
        title = None
        company_name = None
        company_rating = None
        company_reviews = None
        location = None
        location_type = None
        apply_link = None
        pay = None
        job_type = None
        benefits = None
        description = None

        # get the general job data from the outline card
        try:
            date_element = job_card.find_element(By.CSS_SELECTOR, ".date")
            date_element_text = date_element.text
            posted_at_text = date_element_text

            if "•" in date_element_text:
                date_element_text_array = date_element_text.split("•")
                posted_at_text = date_element_text_array[0]
                applications = date_element_text_array[1] \
                    .replace("applications", "") \
                    .replace("in progress", "") \
                    .strip()

            posted_at = posted_at_text \
                .replace("Posted", "") \
                .replace("Employer", "") \
                .replace("Active", "") \
                .strip()
        except NoSuchElementException:
            pass

        # close the anti-scraping modal
        try:
            dialog_element = driver.find_element(By.CSS_SELECTOR, "[role=dialog]")
            close_button = dialog_element.find_element(By.CSS_SELECTOR, ".icl-CloseButton")
            close_button.click()
        except NoSuchElementException:
            pass

        # load the job details card
        job_card.click()

        # wait for the job details section to load after the click
        try:
            title_element = WebDriverWait(driver, 5) \
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-JobInfoHeader-title")))
            title = title_element.text.replace("\n- job post", "")
        except NoSuchElementException:
            continue

        # extract the job details
        job_details_element = driver.find_element(By.CSS_SELECTOR, ".jobsearch-RightPane")

        try:
            company_link_element = job_details_element.find_element(By.CSS_SELECTOR, "div[data-company-name='true'] a")
            company_name = company_link_element.text
        except NoSuchElementException:
            pass

        try:
            company_rating_element = job_details_element.find_element(By.ID, "companyRatings")
            company_rating = company_rating_element.get_attribute("aria-label").split("out")[0].strip()
            company_reviews_element = job_details_element.find_element(By.CSS_SELECTOR, "[data-testid='inlineHeader-companyReviewLink']")
            company_reviews = company_reviews_element.text.replace(" reviews", "")
        except NoSuchElementException:
            pass

        try:
            company_location_element = job_details_element.find_element(By.CSS_SELECTOR,
                                                                        "[data-testid='inlineHeader-companyLocation']")
            company_location_element_text = company_location_element.text

            location = company_location_element_text

            if "•" in company_location_element_text:
                company_location_element_text_array = company_location_element_text.split("•")
                location = company_location_element_text_array[0]
                location_type = company_location_element_text_array[1]
        except NoSuchElementException:
            pass

        try:
            apply_link_element = job_details_element.find_element(By.CSS_SELECTOR, "#applyButtonLinkContainer button")
            apply_link = apply_link_element.get_attribute("href")
        except NoSuchElementException:
            pass

        for div in job_details_element.find_elements(By.CSS_SELECTOR, "#jobDetailsSection div"):
            if div.text == "Pay":
                pay_element = div.find_element(By.XPATH, "following-sibling::*")
                pay = pay_element.text
            elif div.text == "Job Type":
                job_type_element = div.find_element(By.XPATH, "following-sibling::*")
                job_type = job_type_element.text

        try:
            benefits_element = job_details_element.find_element(By.ID, "benefits")
            benefits = []
            for benefit_element in benefits_element.find_elements(By.TAG_NAME, "li"):
                benefit = benefit_element.text
                benefits.append(benefit)
        except NoSuchElementException:
            pass

        try:
            description_element = job_details_element.find_element(By.ID, "jobDescriptionText")
            description = description_element.text
        except NoSuchElementException:
            pass

        # store the scraped data
        job["posted_at"] = posted_at
        job["applications"] = applications
        job["title"] = title
        job["company_name"] = company_name
        job["company_rating"] = company_rating
        job["company_reviews"] = company_reviews
        job["location"] = location
        job["location_type"] = location_type
        job["apply_link"] = apply_link
        job["pay"] = pay
        job["job_type"] = job_type
        job["benefits"] = benefits
        job["description"] = description
        jobs.append(job)

        # wait for a random number of seconds from 1 to 5
        # to avoid rate limiting blocks
        time.sleep(random.uniform(1, 5))

    # increment the scraping counter
    pages_scraped += 1

    # if this is not the last page, go to the next page
    # otherwise, break the while loop
    try:
        next_page_element = driver.find_element(By.CSS_SELECTOR, "a[data-testid=pagination-page-next]")
        next_page_element.click()
    except NoSuchElementException:
        break

# close the browser and free up the resources
driver.quit()

# produce the output object
output = {
    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "jobs": jobs
}

# export it to JSON
with open("jobs.json", "w") as file:
    json.dump(output, file, indent=4)