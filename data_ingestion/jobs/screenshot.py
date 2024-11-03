import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from PIL import Image

def get_site_list(filename):
    list = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for l in lines:
            list.append(l.strip('\n'))
    return list

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

    # Scroll and capture screenshots
    for y_position in tqdm(range(0, total_height, viewport_height), desc="Scrolling"):
        driver.execute_script(f"window.scrollTo(0, {y_position});")
        time.sleep(0.2)  # Allow time for scrolling
        screenshot_path = f"temp_{y_position}.png"
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)

    # Close the driver
    driver.quit()

    # Stitch images together
    stitched_image = stitch_images(screenshots)
    stitched_image.save(output_path)

    # Clean up temporary images
    for path in screenshots:
        os.remove(path)

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

driver = 'C:\Program Files\Google\chromedriver-win64\chromedriver.exe'
output_path = r"C:\Users\Joyce Pascale\PyProjects\manzi-mfa\data_ingestion\jobs\screenshot1.png"
url = get_site_list("list.txt")[0]

print(get_jobs(url, output_path, driver))