import requests
from PIL import Image
import re


def get_image_url(url) -> str:
    response = requests.get(url)
    relative_image_url = re.search('<meta property="og:image" content="(.+?)"', response.text).group(1)
    image_url = url + relative_image_url
    print(image_url)
    return image_url


def crop_image(img):
    """Crop the image to remove the white border."""
    width, height = img.size
    shift = 1100
    ratio = 3
    img = img.crop((shift, 0, height*ratio+shift, height))
    print(f"{img.size} ratio : {img.width/img.height}")
    img.save("image-cropped.jpg")
    return img


def get_image_stream(url: str) -> Image:
    """Get the image stream from the Roundshot website."""
    image_url = get_image_url(url)
    response = requests.get(image_url)
    if response.status_code == 200:
        with open("image.jpg", "wb") as f:
            f.write(response.content)
        img = Image.open("image.jpg")
        return img
    else:
        print("Failed to download image")
        return None


def get_cropped_image_stream(url: str) -> Image:
    """Get the image stream from the Roundshot website."""
    return crop_image(get_image_stream(url))


if __name__ == '__main__':
    crop_image(Image.open("image.jpg"))
