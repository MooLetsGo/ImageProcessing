import numpy as np
import cv2

# Farbbild durch OpenCV Methoden invertieren
def run(image, result,settings=None):
    height, width, channels = image.shape[:]

    result.append({"name":"invertiertesFarbbild","data":255-image})