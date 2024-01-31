import numpy as np
import cv2

# Graubild durch OpenCV-Methoden erzeugen und invertieren
def run(image, result,settings=None):
    height, width, channels = image.shape[:]

    image2=np.zeros((height,width,1)).astype(np.uint8)

    image2=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # Graubild erzeugen

    result.append({"name":"invertiertesGraubild","data":255-image2})