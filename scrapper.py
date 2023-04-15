import requests
from PIL import Image
import re


def get_image_url(url) -> str:
    response = requests.get(url)
    relative_image_url = re.search('<meta property="og:image" content="(.+?)"', response.text).group(1)
    image_url = url + relative_image_url
    return image_url


def get_image_stream(roundshot_website_url: str) -> bytes:
    """Get the image stream from the Roundshot website."""
    url = roundshot_website_url
    image_url = get_image_url(url)
    response = requests.get(image_url)
    if response.status_code == 200:
        with open("image.jpg", "wb") as f:
            f.write(response.content)
        img = Image.open("image.jpg")
        img.show()
        return response.content
    else:
        print("Failed to download image")
        return None
