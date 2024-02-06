import numpy as np
import cv2

def run(image, result,settings=None):

    imageGrey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    #Binärbild erzeugen, bei dem die Farbpunkte weiß sind und der Hintergrund schwarz ist (Helligkeitsgrenzwert=122)
    _,thresh1 = cv2.threshold(imageGrey,130,255,cv2.THRESH_BINARY_INV)
    result.append({"name":"Binaerbild","data":thresh1}) 

    #Konturen (Blobs) aus dem Binärbild extrahieren -> Ausgabe ist eine Liste aus Konturlisten. In den Konturlisten sind alle Pixel
    #Positionen gespeichert, die zu der jeweiligen Kontur gehören
    contours,_ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
    print('space')

    #Kleine Blobs rausfiltern (Aufgabenteil b) )
    contoursgood=[]
    i=0
    for c in contours:
        print(len(c))
        if len(c) >60:
            contoursgood.append(c)
        i +=1
    print(contoursgood)
    
    #Die Konturen werden in einer Kopie vom Originalbild mit Farbe umrandet (0,255,0)
    imageDrawnCont = cv2.drawContours(np.copy(image), contoursgood, -1, (0,255,0), 2)
    result.append({"name":"Blobs","data":imageDrawnCont})

    #Die Konturen werden ausgefüllt
    imageFillPoly=cv2.fillPoly(np.copy(image), contoursgood, (0,255,0))
    result.append({"name":"Gefuellte Blobs","data":imageFillPoly})

if __name__ == '__main__':
    image=cv2.imread("..\Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()