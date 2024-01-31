import numpy as np

# Farbbild durch Pixelmanipulation invertieren
def run(image, result,settings=None):
    height, width, channels = image.shape[:]

    image2=np.zeros((height,width,3)).astype(np.uint8)

    for y in range(height):
        for x in range(width):
                image2[y,x]=(255-image[y,x][0],255-image[y,x][1],255-image[y,x][2])
    result.append({"name":"invertiertesFarbbild","data":image2})