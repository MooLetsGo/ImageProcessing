import numpy as np
import cv2

def run(image, result,settings=None):
    
    #Graubild oder Farbbild nehemen?
    image= cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    img_normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    
    height = img_normalized.shape[0]
    width = img_normalized.shape[1]
    img_pseudo=np.zeros((height,width,3)).astype(np.uint8)
    for row in range(height):
        for col in range(width):
            grey = img_normalized[row, col]#[0]
            if 26 > row & row > 4:
                 if width - 12 > col & col > 11:
                    grey = 255 * (col - 12) / (width - 25)

            img_pseudo[row, col][2] = -np.sin(grey/256*2*np.pi)*127.9+128
            img_pseudo[row, col][1] = -np.cos(grey/256*2*np.pi)*127.9+128
            img_pseudo[row, col][0] =  np.sin(grey/256*2*np.pi)*127.9+128
    
    result.append({"name":"PseudoColor","data":img_pseudo})

if __name__ == '__main__':
    image=cv2.imread("Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()