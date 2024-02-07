import numpy as np
import cv2

def run(image, result,settings=None):

    imageGrey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _,thresh1 = cv2.threshold(imageGrey,10,255,cv2.THRESH_BINARY)
    
    contours,_ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    imageDrawnCont = cv2.drawContours(np.copy(image), contours, -1, (0,255,0), 2)
    result.append({"name":"Blobs","data":imageDrawnCont})
    

if __name__ == '__main__':
    image=cv2.imread("..\Images\Objekte.png")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()