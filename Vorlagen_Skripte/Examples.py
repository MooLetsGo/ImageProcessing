import numpy as np
import cv2

def run(image, result,settings=None):
    height, width, channels = image.shape[:]
    
    #Zeichnen auf Bild
    imageD=image.copy()
    cv2.rectangle(imageD, (10,10), (255, 100), (255, 0, 0), 2)
    cv2.circle(imageD, (100,100), 40, (255, 0, 100), 2)
    cv2.putText(imageD, "H:"+str(height)+" W:"+str(width)+" C:"+str(channels)+" T:"+str(image.dtype),  (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.3,  (100, 0, 100), 1, cv2.LINE_AA)
    result.append({"name":"Draw","data":imageD})

    #Bild auf Pixelebene manipulieren
    image2=np.zeros((height,width,3)).astype(np.uint8)
    for y in range(height):
        for x in range(width):
            image2[y,x]=(y,int(x),image[y,x][2])
    result.append({"name":"yx","data":image2})

    #Graubild erzeugen
    image3=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY); 
    result.append({"name":"Gray","data":image3})
    
    #Sinus darstellen
    sinMat = np.fromfunction(lambda x, y: np.cos((x+y)/10.0)*0.5+0.5, (512, 512), dtype=float)
    result.append({"name":"Sin","data":sinMat})

    #Umgang mit Kanälen
    _,_,red=cv2.split(image)
    zero=np.zeros((height,width),np.uint8)
    result.append({"name":"Red","data":red})
    image4=cv2.merge((zero,zero,red))
    result.append({"name":"Red2","data":image4})

    #Homogene Pixeloperationen
    image5=image/512+0.5
    print(image.dtype,image5.dtype)
    result.append({"name":"HomogenFloat","data":image5})
    result.append({"name":"HomogenUint8","data":(image/2+127.5).astype(np.uint8)})

    #Matrizen verbinden
    result.append({"name":"Resize_Concat","data":np.concatenate((cv2.resize(image4,(300,300)), cv2.resize(image,(300,300))), axis=1)})


if __name__ == '__main__':
    image=cv2.imread("Images\Farbpunkte.jpg")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()