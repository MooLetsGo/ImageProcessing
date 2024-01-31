import numpy as np
import cv2


def run(image, result,settings=None):
    
    b,g,r = cv2.split(image)
    #Min und Max werte aus den einzelnen Kanälen rausholen
    minB,maxB,_,_=cv2.minMaxLoc(b)
    minG,maxG,_,_=cv2.minMaxLoc(g)
    minR,maxR,_,_=cv2.minMaxLoc(r)

    #Globalen Min und Max Wert aus allen Min und Max Werten der Kanäle bestimmen -> deswegen global
    max=np.max((maxB,maxG,maxR))
    min=np.min((minB,minG,minR))

    #Kontrastspreizung kanalweise aber mit den globalen Min und Max Werten durchführen
    b = ((255/(max-min))*(b-min)).astype(np.uint8)
    g = ((255/(max-min))*(g-min)).astype(np.uint8)
    r = ((255/(max-min))*(r-min)).astype(np.uint8)

    #Carsten Variante:
    #imagespreiz = image.copy()
    #imagespreiz = ((255/(max-min))*(imagespreiz-min)).astype(np.uint8)

    imageSpread=cv2.merge((b,g,r))
    result.append({"name":"Spreaded","data":imageSpread})

    img_normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    result.append({"name":"Spreaded with openCV Function","data":img_normalized})
    
if __name__ == '__main__':
    image=cv2.imread("Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()