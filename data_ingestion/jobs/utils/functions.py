import base64
from openai import OpenAI
from models.job import Jobs
from PIL import Image

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

def analyze_screenshot(image_path):
    """Analyse une capture d'écran pour extraire les titres et lieux des emplois même s'il semble y avoir des doublons."""
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
