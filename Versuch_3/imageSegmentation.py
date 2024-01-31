import numpy as np
import cv2

def filter(image, classFilter):
    height = image.shape[0]
    width = image.shape[1]
    img_normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    b, g, r = cv2.split(img_normalized)
    #classYellowMarker = (255,255,255)

    image2=np.zeros((height,width,3),np.uint8)
    #Prüft Pixelweise die BGR werte. True wenn alle BGR werte im Filterbereich liegen
    image2[((classFilter[0][0] >= b)&(b >= classFilter[1][0])) & ((classFilter[0][1] >= g)&(g >= classFilter[1][1])) & ((classFilter[0][2] >= r)&(r >= classFilter[1][2]))] = (255,255,255)
    return image2

def run(image, result,settings=None):

    #Filteraufbau
    #[bmax gmax rmax]
    #[bmin gmin rmin]
    #bgr Wertebereiche für die Farben: http://www.markusbader.de/tricky/rgb_blau.html
    filterClassYellow = np.array([[224,255,255],[0,105,139]])
    filterClassBlue = np.array([[255,255,240],[112,0,0]])


    result.append({"name":"Original","data":image})
    result.append({"name":"Filter Gelb","data":filter(image,filterClassYellow)})
    result.append({"name":"Filter Blau","data":filter(image,filterClassBlue)})

if __name__ == '__main__':
    image=cv2.imread("Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()