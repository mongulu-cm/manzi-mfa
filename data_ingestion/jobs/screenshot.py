import os
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from PIL import Image
import platform
from openai import OpenAI
import json
import base64
from pydantic import BaseModel
from tabulate import tabulate

class Job(BaseModel):
    title: str
    location: str

class Jobs(BaseModel):
    jobs: list[Job]

system_prompt = '''
    You are an agent specialized in checking if an image contains jobs title and location. If it's the case, you are able to extract them all.
    You will be provided an image, and your goal is to extract all jobs title and location if exists.
'''

def get_site_list(filename):
    list = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for l in lines:
            list.append(l.strip('\n'))
    return list

def get_positions(url, driver_path):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialiser le driver Chrome
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(2)

    # Obtenir les dimensions initiales
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    # Ajouter un écouteur d'événements pour le clic
    driver.execute_script("""
        document.addEventListener('click', function(e) {
            const scrollPosition = window.pageYOffset;
            const relativeX = e.clientX;
            const relativeY = e.clientY + scrollPosition;

            console.log('Position relative : X=' + relativeX + ', Y=' + relativeY);
            console.log('Position relative au viewport : Y=' + (relativeY % """ + str(viewport_height) + """));
            console.log('Numéro de viewport : ' + Math.floor(relativeY / """ + str(viewport_height) + """));
        });
    """)

    # Garder le navigateur ouvert indéfiniment
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nFermeture du navigateur...")
        driver.quit()


def click_on_next(url, driver_path, x, y):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialiser le driver Chrome
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(2)

    try:
        page_count = 0
        last_page_content = ""

        while True:
            try:
                # Obtenir le contenu de la page avant le clic
                current_page_content = driver.page_source

                # Si le contenu n'a pas changé après le dernier clic, on est probablement à la fin
                if current_page_content == last_page_content:
                    print("Contenu de page identique détecté - Fin de la pagination atteinte")
                    break

                # Sauvegarder le contenu actuel pour la prochaine comparaison
                last_page_content = current_page_content

                # Calculer la position de défilement nécessaire
                viewport_height = driver.execute_script("return window.innerHeight")
                scroll_position = (y // viewport_height) * viewport_height

                # Faire défiler jusqu'à la position correcte
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(0.5)

                # Créer un objet ActionChains pour le clic
                actions = ActionChains(driver)

                # Calculer la position Y relative au viewport
                relative_y = y % viewport_height

                # Effectuer le clic aux coordonnées spécifiées
                actions.move_by_offset(x, relative_y).click().perform()
                page_count += 1
                print(f"Clic effectué sur la page {page_count}")

                # Attendre 10 secondes avant le prochain clic
                time.sleep(10)

                # Réinitialiser la position du curseur
                actions.move_by_offset(-x, -relative_y).perform()

            except Exception as e:
                print(f"Erreur lors du clic : {e}")
                break

    finally:
        print(f"Navigation terminée après {page_count} pages")
        driver.quit()

def get_jobs(url, output_path, driver_path):
    """Capture a full-page screenshot of the given URL by scrolling and stitching images together."""
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the Chrome driver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    try:
        cookie_decline_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonDecline"))
        )
        cookie_decline_button.click()
    except:
        print("Cookie decline button not found or not clickable.")

    # Get the total scroll height and the viewport height
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    # List to store partial screenshots
    screenshots = []
    all_jobs = []

    # Scroll and capture screenshots
    for y_position in tqdm(range(0, total_height, viewport_height), desc="Scrolling"):
        driver.execute_script(f"window.scrollTo(0, {y_position});")
        time.sleep(0.2)  # Allow time for scrolling
        screenshot_path = f"temp_{y_position}.png"
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)
        jobs_data = analyze_screenshot(screenshot_path)
        if jobs_data:
            jobs_dicts = [{"title": job.title, "location": job.location} for job in jobs_data.jobs]
            all_jobs.extend(jobs_dicts)


    # Close the driver
    driver.quit()

    # Stitch images together
    stitched_image = stitch_images(screenshots)
    stitched_image.save(output_path)

    # Clean up temporary images
    for path in screenshots:
        os.remove(path)

    print(tabulate(all_jobs, headers="keys", tablefmt="grid"))


def analyze_screenshot(image_path):
    """Analyse une capture d'écran pour extraire les titres et lieux des emplois."""
    client = OpenAI()

    with open(image_path, "rb") as image_file:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": system_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode()}"
                            }
                        }
                    ]
                }
            ],
            response_format=Jobs,
        )


        message = response.choices[0].message
        if message.parsed:
            print(message.parsed)
            return message.parsed
        else:
            print(message.refusal)
            return []

def stitch_images(image_paths):
    """Stitch multiple images vertically into a single image."""
    images = [Image.open(img_path) for img_path in image_paths]
    width, total_height = images[0].size[0], sum(img.size[1] for img in images)

    stitched_image = Image.new("RGB", (width, total_height))
    y_offset = 0
    for img in images:
        stitched_image.paste(img, (0, y_offset))
        y_offset += img.size[1]

    return stitched_image



# Take screenshot and save it
#driver.save_screenshot(r"C:\Users\Joyce Pascale\PyProjects\manzi-mfa\data_ingestion\jobs\screenshot1.png")
#driver.quit()

# Déterminer le chemin du driver en fonction du système d'exploitation
if platform.system() == 'Windows':
    driver = r'C:\Program Files\Google\chromedriver-win64\chromedriver.exe'  # Notez le 'r' pour raw string
elif platform.system() == 'Darwin':  # Darwin est le nom du système pour macOS
    driver = '/opt/homebrew/bin/chromedriver'
else:
    driver = '/usr/local/bin/chromedriver'  # Pour Linux

output_path = r"C:\Users\Joyce Pascale\PyProjects\manzi-mfa\data_ingestion\jobs\screenshot1.png"
url = get_site_list("list.txt")[0]

print(get_jobs(url, output_path, driver))
# print(get_positions(url,driver))
# print(click_on_next(url, driver, 810, 2089))

