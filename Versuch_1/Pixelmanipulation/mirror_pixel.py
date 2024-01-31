import numpy as np

#Bild durch Pixelmanipulation spiegeln
def run(image, result,settings=None):
    height, width, channels = image.shape[:]

    image2=np.zeros((height,width,3)).astype(np.uint8)

    for y in range(height):
        for x in range(width):
            image2[y,x]=image[y,width-x-1]
    result.append({"name":"gespiegelt","data":image2})