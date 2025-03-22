import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_site_list(filename):
    list = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for l in lines:
            list.append(l.strip('\n'))
    return list


def get_jobs(url):
    # Send a request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract job information
        jobs = []
        
        # Finding job sections
        job_sections = soup.find_all('div', class_='jet-listing-grid__item')  # You may need to adjust the class name based on HTML structure
        
        for section in job_sections:
            job_url = section.find('a', class_='jet-engine-listing-overlay-link')['href']
            job_title = section.find('div', class_='jet-listing-dynamic-field__content').text.strip()  # Extract job title
            location = section.find('span', class_='jet-listing-dynamic-terms__link').text.strip()  # Extract job location
            job_type = section.find_all('div', class_='jet-listing-dynamic-field__content')[1].text.strip()  # Extract job type
            jobs.append({'Job Title': job_title, 'Location': location, 'Job Type': job_type, 'Job URL':job_url})

        # Convert job data into a DataFrame
        df = pd.DataFrame(jobs)
    else:
        print("Failed to retrieve the webpage")

    return df

def get_jobs_pages(url):
    service = Service('C:\Program Files\Google\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    jobs = []

    while True:
        # Wait for job listings to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'jet-listing-grid__item'))) 

        # Parse the current page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_sections = soup.find_all('div', class_='jet-listing-grid__item')
        
        # Extract job information as before
        for section in job_sections:
            job_url = section.find('a', class_='jet-engine-listing-overlay-link')['href']
            job_title = section.find('div', class_='jet-listing-dynamic-field__content').text.strip()  # Extract job title
            location = section.find('span', class_='jet-listing-dynamic-terms__link').text.strip()  # Extract job location
            job_type = section.find_all('div', class_='jet-listing-dynamic-field__content')[1].text.strip()  # Extract job type
            jobs.append({'Job Title': job_title, 'Location': location, 'Job Type': job_type, 'Job URL':job_url})

        # Find and click the "Next" button
        print("Trying")
        pagination_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.jet-smart-filters-pagination.jet-filter')))
        #print(pagination_div.get_attribute("innerHTML"))
        # Wait for the "Next" button to be clickable inside the pagination div
        #next_button = pagination_div.find_element(By.XPATH, ".//a[normalize-space()='Next']")
        next_button = WebDriverWait(pagination_div, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.jet-filters-pagination__item.prev-next.next")))
        # Click the "Next" button
        next_button.click()
        time.sleep(15)  # Wait for AJAX content to load
        print('Done')

    driver.quit()
    # Convert job data into a DataFrame
    df = pd.DataFrame(jobs)
    return df


print(get_jobs_pages(get_site_list("list.txt")[1]))