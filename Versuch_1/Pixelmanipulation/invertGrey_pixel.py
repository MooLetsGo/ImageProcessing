import numpy as np

# Graubild durch Pixelmanipulation invertieren
def run(image, result,settings=None):
    height, width, channels = image.shape[:]

    image2=np.zeros((height,width,1)).astype(np.uint8)

    # In image2 das Graubild von image speichern
    for y in range(height):
        for x in range(width):
            # Jeder Pixel von image hat einen bgr Wert -> [0]=b,[1]=g,[2]=r -> mit aus der Summe der Werte mit den entsprechenden
            # Faktoren ergibt sich der Grau Wert für das 1-kanalige image2
            image2[y,x]=(0.11*image[y,x][0]+0.59*image[y,x][1]+0.3*image[y,x][2])

    # Grauwerte von image2 invertieren
    for y in range(height):
        for x in range(width):
            image2[y,x]=(255-image2[y,x]) # 255 weil jeder pixel 8-bit hat
    result.append({"name":"invertiertesGraubild","data":image2})