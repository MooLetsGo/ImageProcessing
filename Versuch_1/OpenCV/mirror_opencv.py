import numpy as np
import cv2

# Bild an y-Achse mit der Methode flip() spiegeln
def run(image, result,settings=None):
    height, width, channels = image.shape[:]

    image2=np.zeros((height,width,3)).astype(np.uint8)
    
    cv2.flip(image,1,image2) # cv2.flip(Source, an welcher Achse (0=x, 1=y, -1=beide), Destination)
    result.append({"name":"gespiegelt","data":image2})