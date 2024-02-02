import numpy as np
import cv2

def run(image, result,settings=None):
    
    blue,green,red=cv2.split(image)
        
    lowest=np.min(red)
    highest=np.max(red)
    #redSpread ist eine Matrix, bei der die Werte von lowest und highest gemäß der Verrechnung
    #aufgesplittet wurden. Der Wertebereich von den Zahlen in redSpread liegt dabei zwischen 0 und 1. 
    #Eine Umwandlung des Wertebereiches wieder in 0-255 würde so funktionieren: (255*redSpread).astype(np.uint8)
    redSpread = ((red-lowest)/(highest-lowest)) 
    

    lowest=np.min(green)
    highest=np.max(green)
    greenSpread = ((green-lowest)/(highest-lowest))

    lowest=np.min(blue)
    highest=np.max(blue)
    blueSpread = ((blue-lowest)/(highest-lowest))
    
    image4=cv2.merge((blueSpread,greenSpread,redSpread))
    result.append({"name":"Spreaded","data":image4})

if __name__ == '__main__':
    image=cv2.imread("Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()