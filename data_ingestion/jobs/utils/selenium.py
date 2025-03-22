import platform
import tempfile
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
from .functions import analyze_screenshot

def setup_chrome_driver(driver_path: str) -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=960,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def get_positions(url, driver_path):
    driver = setup_chrome_driver(driver_path)
    driver.get(url)
    time.sleep(2)
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    driver.execute_script(f"""
        document.addEventListener('click', function(e) {{
            const scrollPosition = window.pageYOffset;
            const relativeX = e.clientX;
            const relativeY = e.clientY + scrollPosition;
            console.log('Position relative : X=' + relativeX + ', Y=' + relativeY);
            console.log('Position relative au viewport : Y=' + (relativeY % {viewport_height}));
            console.log('Numéro de viewport : ' + Math.floor(relativeY / {viewport_height}));
        }});
    """)
    try:
        print("\nRegardez la console du navigateur pour obtenir les coordonnées...")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nFermeture du navigateur...")
        driver.quit()

def get_driver_path():
    if platform.system() == 'Windows':
        driver_path = r'C:\Program Files\Google\chromedriver-win64\chromedriver.exe'  # Notez le 'r' pour raw string
    elif platform.system() == 'Darwin':  # Darwin est le nom du système pour macOS
        driver_path = '/opt/homebrew/bin/chromedriver'
    else:
        driver_path = '/usr/local/bin/chromedriver'

    return driver_path

def scroll_and_extract_jobs(driver, all_jobs, screenshots):
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

                # Capture et analyse de la page courante
    for y_position in tqdm(range(0, total_height, viewport_height), desc="Scrolling"):
        driver.execute_script(f"window.scrollTo(0, {y_position});")
        time.sleep(0.2)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            screenshot_path = temp_file.name
            driver.save_screenshot(screenshot_path)
            screenshots.append(screenshot_path)

        jobs_data = analyze_screenshot(screenshot_path)
        if jobs_data:
            jobs_dicts = [{"title": job.title, "location": job.location} for job in jobs_data.jobs]
            all_jobs.extend(jobs_dicts)