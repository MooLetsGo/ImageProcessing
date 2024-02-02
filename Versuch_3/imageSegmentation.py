import numpy as np
import cv2

def mulPixelWithFactor(factor: float,image):
    width = image.shape[1]
    height = image.shape[0]
    for y in range (height):
        for x in range (width):
            image[y,x] = image[y,x]*factor
    
    return image

def filter(image, classFilter):
    height = image.shape[0]
    width = image.shape[1]
    img_normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    b, g, r = cv2.split(img_normalized)
    #----------------------Weißabgleich----------------------#

    #hellsten Pixel der Kanäle bestimmen
    bMax = np.max(b)
    gMax = np.max(g)
    rMax = np.max(r)

    #Faktor der Kanäle bestimmen
    kb = 255/bMax
    kg = 255/gMax
    kr = 255/rMax

    b = mulPixelWithFactor(kb,b)
    g = mulPixelWithFactor(kg,g)
    r = mulPixelWithFactor(kr,r)

    #--------------------------------------------------------#

    image2=np.zeros((height,width,3),np.uint8)
    #Prüft Pixelweise die BGR werte. True wenn alle BGR werte im Filterbereich liegen -> Farbe Weiß wird diesen Pixeln zugewiesen
    image2[((classFilter[0][0] >= b)&(b >= classFilter[1][0])) & ((classFilter[0][1] >= g)&(g >= classFilter[1][1])) & ((classFilter[0][2] >= r)&(r >= classFilter[1][2]))] = (255,255,255)
    
    return image2

def run(image, result,settings=None):
    print(image[0,0])

    #Filteraufbau
    #[bmax gmax rmax]
    #[bmin gmin rmin]
    #bgr Wertebereiche für die Farben: http://www.markusbader.de/tricky/rgb_blau.html
    filterClassYellow = np.array([[settings[0],255,255],[settings[1],105,139]])
    filterClassBackround = np.array([[144,130,112],[134,120,112]])#pixel[0,0]=[139 125 107] -> +-5 bei Filter
    #filterClassBlue = np.array([[255,255,240],[112,0,0]])
    #filterClassBlueVio = np.array([[255,255,255],[96,0,0]])


    result.append({"name":"Original","data":image})
    result.append({"name":"Filter Gelb","data":filter(image,filterClassYellow)})
    result.append({"name":"Filter Hintergrund","data":filter(image,filterClassBackround)})
    #result.append({"name":"Filter Gelb Costum","data":filter(image,filterClassYellowCostum)})
    #result.append({"name":"Filter Blau Violett","data":filter(image,filterClassBlueVio)})

if __name__ == '__main__':
    image=cv2.imread("Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()