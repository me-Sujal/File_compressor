# utils/image_handler.py
import numpy as np
from PIL import Image

class ImageHandler:
    @staticmethod
    def read_image(filepath):
        with Image.open(filepath) as img:
            return np.array(img.convert('L'))
            
    @staticmethod
    def save_image(filepath, data):
        if isinstance(data, np.ndarray):
            Image.fromarray(data).save(filepath)
        else:
            Image.fromarray(np.array(data)).save(filepath)
