import requests
from bs4 import BeautifulSoup
import pandas as pd

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

print(get_jobs(get_site_list("list.txt")[1]))