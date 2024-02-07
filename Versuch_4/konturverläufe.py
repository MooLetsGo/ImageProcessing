import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math as m

#Hilfsfunktionen für die Schwerpunktbestimmung
def momentBerechnung(ohm,i,j):
    moment = 0
    for konturpixel in ohm:
        x = konturpixel[0][0]
        y = konturpixel[0][1]
        moment += (x**i)*(y**j)
    return moment

def zentralmomentBerechnung(ohm,i,j,xs,ys):
    zentralmoment = 0
    for konturpixel in ohm:
        x = konturpixel[0][0]
        y = konturpixel[0][1]
        zentralmoment += ((x-xs)**i)*((y-ys)**j)
    return zentralmoment

#Hilfsfunktionen für die Polarkoordinaten Berechnung
def radius(konturpixel,xs,ys):
    x = konturpixel[0][0]
    y = konturpixel[0][1]
    return np.sqrt((y-ys)**2+(x-xs)**2)

def winkel(konturpixel,xs,ys):
    x = konturpixel[0][0]
    y = konturpixel[0][1]
    gk = (y-ys)
    ak = (x-xs)
    if ak<0 and gk<0:
        return np.pi + np.arctan2(gk,ak)
    elif ak<0 and gk>0:
        return np.pi + np.arctan2(gk,ak)
    elif ak>0 and gk>0:
        return np.pi + np.arctan2(gk,ak)
    else:
        return np.arctan2(gk,ak)

#----------------------------------------------------------------------------------------------------------#
    
def run(image, result,settings=None):
#Segmentierung
    imageGrey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _,thresh1 = cv2.threshold(imageGrey,10,255,cv2.THRESH_BINARY)
    contours,_ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    imageSegmented = cv2.drawContours(np.copy(image), contours, -1, (0,255,0), 2)
    
    
#Schwerpunktbestimmung mit normalen Momenten für den ersten Blob im contours-Array
    ohm=contours[0]
    #print(ohm[0][0][x,y])
    m00 = momentBerechnung(ohm,0,0)
    m10 = momentBerechnung(ohm,1,0)
    m01 = momentBerechnung(ohm,0,1)
    #Schwerpunkt Koordinaten
    ys=m01/m00
    xs=m10/m00
    #--Ausgabe--#
    #imgSpMitMoment = np.copy(imageSegmented)
    #imgSpMitMoment[int(ys),int(xs)]=[0,0,255]
    #result.append({"name":"SpMitMoment","data":imgSpMitMoment})

#Schwerpunktbestimmung mit Zentralmomenten für den ersten Blob im contours-Array ???--Geht noch nicht--???
    zm00 = zentralmomentBerechnung(ohm,0,0,xs,ys)
    zm10 = zentralmomentBerechnung(ohm,1,0,xs,ys)
    zm01 = zentralmomentBerechnung(ohm,0,1,xs,ys)
    zmYs=zm01/zm00
    zmXs=zm10/zm00

#Konturverlauf in Polarkoordinatendarstellung um den Schwerpunkt des ersten Blobs im contours-Array
    xVerlauf = np.zeros(len(ohm))
    for i, konturpixel in enumerate(ohm):
        r = radius(konturpixel, xs, ys) 
        phi = winkel(konturpixel, xs, ys)
        xVerlauf[i] = r * np.cos(phi)
    result.append({"name":"Plot","data":xVerlauf})
    





if __name__ == '__main__':
    matplotlib.use('Agg')
    image=cv2.imread("..\Images\Objekte.png")
    result=[]
    run(image,result)
    for ele in result:
        if(len(ele["data"].shape)==1):
            fig=plt.figure(num=ele["name"])
            plt.plot(ele["data"])
            fig.tight_layout()
            plt.grid(True)
            plt.xlim(0.0, len(ele["data"])-1)
            fig.canvas.draw()
            data = np.array(fig.canvas.renderer._renderer)
            cv2.imshow(ele["name"],data)
        else:
            cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()