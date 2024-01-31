import numpy as np
import cv2



def pixelValues(x,y):
    height, width =(500,500)
    dx, dy = (width/2-x, height/2-y)
    r=np.sqrt(dx**2+dy**2)
    a=np.arctan2(dy,dx)
    # weil die np.fromfunction() die Matrix mit float Werten aufbaut --> Kosinus Werte müssen
    # von 0-1 laufen --> deswegen *0.5 und +0.5
    return (np.cos(r**1.4/50+a)*0.5)+0.5

def run(image, result,settings=None):
    
    #Variante 1
    #Matrix für Bild mit rotationssymmetrischen Kosinus erstellen und dieses generieren
    cosMat = np.fromfunction(lambda x,y : pixelValues(x,y), (500,500)) #(y,x)
    result.append({"name":"rotSymCos_float","data":cosMat})

    #Variante 2
    #Bild Pixelweise durch eine geschachtelte Schleife generieren
    height, width =(500,500)
    image2=np.zeros((height,width,1)).astype(np.uint8)
    for y in range(height):
        for x in range(width):
            dx, dy = (width/2-x, height/2-y)
            r=np.sqrt(dx**2+dy**2)
            a=np.arctan2(dy,dx)
            image2[y,x]=(np.cos(r**1.4/50+a)+1)*127.49
    #result.append({"name":"rotSymCos_uint8","data":image2})

#Um Bilder zu generieren, ohne die GUI zu verwenden
if __name__ == '__main__':
    image=cv2.imread("..\..\Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()