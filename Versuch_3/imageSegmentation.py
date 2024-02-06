import numpy as np
import cv2

def filter(image, classFilter, classFarbe):
    height = image.shape[0]
    width = image.shape[1]
    b, g, r = cv2.split(image)
   
    image2=np.zeros((height,width,3),np.uint8)
    #Prüft Pixelweise die BGR werte. True wenn alle BGR werte im Filterbereich liegen -> Farbe Weiß wird diesen Pixeln zugewiesen
    image2[((classFilter[0][0] >= b)&(b >= classFilter[1][0])) & ((classFilter[0][1] >= g)&(g >= classFilter[1][1])) & ((classFilter[0][2] >= r)&(r >= classFilter[1][2]))] = classFarbe
    
    return image2

def run(image, result,settings=None):
    
    #Filteraufbau
    #[bmax gmax rmax]
    #[bmin gmin rmin]
    filterYellow = np.array([[87,143,150],[27,100,103]])
    filterBlue = np.array([[104,60,85],[63,20,0]])
    filterOrange = np.array([[95,91,145],[0,20,110]])
    filterRot = np.array([[69,57,95],[0,0,60]])
    filterGrün = np.array([[76,87,10],[40,50,0]])
    filterHintergrund = np.array([[179,164,140],[129,120,100]])

    #Markierungsfarben die den gefilterten Bereichen (Klassen) zugewiesen werden
    #bgr Wertebereiche für die Farben: http://www.markusbader.de/tricky/rgb_blau.html
    klasseGelb = (0,255,255)
    klasseBlau = (238,0,0)
    klasseOrange = (0,127,255)
    klasseRot = (0,0,238)
    klasseGrün = (0,255,0)
    klasseHintergrund = (255,255,255)

        
    result.append({"name":"Filter Gelb","data":filter(image,filterYellow, klasseGelb)})
    result.append({"name":"Filter Blau","data":filter(image,filterBlue, klasseBlau)})
    result.append({"name":"Filter Orange","data":filter(image,filterOrange, klasseOrange)})
    result.append({"name":"Filter Rot","data":filter(image,filterRot, klasseRot)})
    result.append({"name":"Filter Grün","data":filter(image,filterGrün, klasseGrün)})
    result.append({"name":"Filter Hintergrund","data":filter(image,filterHintergrund, klasseHintergrund)})

    all=filter(image,filterYellow, klasseGelb)+filter(image,filterBlue, klasseBlau)+filter(image,filterOrange, klasseOrange)+filter(image,filterRot, klasseRot)+filter(image,filterGrün, klasseGrün)+filter(image,filterHintergrund, klasseHintergrund)
    result.append({"name":"Filter Alle 6 Klassen","data":all})

if __name__ == '__main__':
    image=cv2.imread("Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()