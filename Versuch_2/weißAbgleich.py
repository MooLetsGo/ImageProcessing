import numpy as np
import cv2

def mulPixelWithFactor(factor: float,image):
    width = image.shape[1]
    height = image.shape[0]
    for y in range (height):
        for x in range (width):
            image[y,x] = image[y,x]*factor
    
    return image

def run(image, result,settings=None):
    #Originalbild ausgeben
    result.append({"name":"Original","data":image})

#Weißabgleich mit Graubild----------------------------------------------
    #hellsten Pixel im Bild suchen
    img_grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    max = np.max(img_grey)
    
    #Faktor bestimmen
    k = 255/max

    #Faktor auf alle Pixel anwenden
    result.append({"name":"Weissabgleich Graubild","data":mulPixelWithFactor(k,img_grey)})

#Weißabgleich mit Farbbild----------------------------------------------
    #hellsten Pixel der Kanäle suchen
    b,g,r = cv2.split(image)
    bMax = np.max(b)
    gMax = np.max(g)
    rMax = np.max(r)

    #Faktor der Kanäle bestimmen
    kb = 255/bMax
    kg = 255/gMax
    kr = 255/rMax

    #Faktor auf alle Pixel anwenden
    b = mulPixelWithFactor(kb,b)
    g = mulPixelWithFactor(kg,g)
    r = mulPixelWithFactor(kr,r)

    image_color = cv2.merge((b,g,r))
    result.append({"name":"Weissabgleich Farbbild","data":image_color})

if __name__ == '__main__':
    image=cv2.imread("Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()