"""Pillow image access used by the original steganography classes."""
from PIL import Image


class ImgC:
    def __init__(self, image_path):
        self.image_path = image_path
        with Image.open(image_path) as source:
            self.Img = source.convert("RGBA")

    def byteammount(self):
        width, height = self.Img.size
        return width * height * 4, width, height

    def getpixel(self, x):
        return self.Img.getpixel(x)

    def setpixel(self, x, value):
        self.Img.putpixel(x, value)

    def save(self, path):
        self.Img.save(path, format="PNG")
