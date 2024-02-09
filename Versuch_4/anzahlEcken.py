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

def koordinatenSchwerpunkt(ohm):
    m00 = momentBerechnung(ohm,0,0)
    m10 = momentBerechnung(ohm,1,0)
    m01 = momentBerechnung(ohm,0,1)
    ys=m01/m00
    xs=m10/m00
    return xs,ys

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
    return np.arctan2(gk,ak)

#------------------------------------Funktion Berechnung Konturverlauf-------------------------------------------------------#
def konturVerlauf(ohm):
    #(ohm[0][0][x,y])
    #Schwerpunkt Koordinaten
    xs,ys= koordinatenSchwerpunkt(ohm)
    #Konturverlauf in Polarkoordinatendarstellung um den Schwerpunkt des ersten Blobs im contours-Array
    bins=80
    Verlauf = np.ones(bins)*(-1)
    for _, konturpixel in enumerate(ohm):
        r = radius(konturpixel, xs, ys) 
        phi = winkel(konturpixel, xs, ys)
        Verlauf[int((phi/np.pi+1)*(bins*0.99999)/2)] = r
    return Verlauf
#----------------------------------------------------------------------------------------------------------------------------#

def run(image, result,settings=None):
#Segmentierung
    imageGrey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _,thresh1 = cv2.threshold(imageGrey,10,255,cv2.THRESH_BINARY)
    contours,_ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  

#Geglättete Konturverläufe der einzelnen Objekte in einer Liste speichern
    konturVerläufe = []
    fensterbreite = np.ones(3) / 3
    for kontur in contours:
        verlauf_smooth=np.convolve(konturVerlauf(kontur), fensterbreite, mode='valid') #np.convlove wird zum Glätten der Funktion benutzt (Faltung -> Funktionsweise evtl. nochmal anschauen)
        konturVerläufe.append(verlauf_smooth)

#Liste generieren, die für jeden Konturverlaufes eines Objektes die Anzahl der Hochpunt speichert
    anzahlHochpunkte = []
    for kv in konturVerläufe:
        #Für jede Objektkontur die Hochpunktpositionen bestimmen und in einer Liste speichern
        hochpunktePos=[]
        for i in range(len(kv)):
            #Abfrage, ob die Nachbarwerte des aktuellen Wertes kleiner sind -> wenn ja dann ist der aktuelle Wert ein HP
            #Modulo Opertion liefert für das letzte Element in einer kv-Liste den Wert 0 -> letztes Element wird mit erstem verglichen
            #-> macht Sinn, da durch die Polarkoordinatendarstellung der letzte und der erste Wert Nachbarn sind (Kreisbetrachtung)
            #Für das erste Element einer kv-Liste erkennt Python bei dem Statement kv[i-1] automatisch, dass hier mit dem letzten Wert 
            #der Liste verglichen werden soll 
            if (kv[i]>kv[(i+1)%len(kv)]) and (kv[i]>kv[i-1]):
                hochpunktePos.append(i) 
        #Länge von hochpunktePos-Liste entspricht der Anzahl der HPs der jeweiligen Kontur -> Anzahl HPs = Anzhal Ecken!!
        anzahlHochpunkte.append(len(hochpunktePos))

#Ecken Anzahl für jedes Objekt passend im Bild eintragen 
    #Farbe und Schriftart definieren
    color = (0, 0, 255)  
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    # Text auf das Bild zeichnen
    i=0
    for v in anzahlHochpunkte:
        #Textposition
        xs,ys=koordinatenSchwerpunkt(contours[i])
        #Funktion zum Zeichnen in Bildern
        cv2.putText(image, str(v), (int(xs)-10, int(ys)+10), font, font_scale, color, thickness)
        i+=1
        
#Ausgabe
    result.append({"name":"Draw","data":image})
       
        
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



