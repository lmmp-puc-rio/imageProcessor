#save button
from PIL import Image

def resize_image(image, maxsize):
    r1 = image.size[0]/maxsize[0] # width ratio
    r2 = image.size[1]/maxsize[1] # height ratio
    ratio = max(r1, r2)
    newsize = (int(image.size[0]/ratio), int(image.size[1]/ratio))
    image = image.resize(newsize, Image.LANCZOS)
    return image

def resize_image_predifined(image, size):
    newsize = (int(size[0]), int(size[1]))
    image = image.resize(newsize, Image.LANCZOS)
    return image