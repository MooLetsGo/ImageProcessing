import numpy as np
import cv2

def run(image, result,settings=(2,50)):

    #------------------------Bild mit SVM segmentieren---------------------------#
    if(len(image.shape)!=3):
            print("Nur für Farbbilder")
            return
    height, width, *_ = image.shape[:]  # image height and width

    svm = cv2.ml.SVM_create()
    svm.setKernel(cv2.ml.SVM_LINEAR)
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setC(settings[0]/10+0.1)
    svm.setGamma(settings[0]/10.0+0.1)

    
    rows=np.array((154, 101,  10),dtype=np.float32)#hellblau
    rows = np.vstack((rows,np.array((73, 42,  9),dtype=np.float32)))#dunkelblau
    

    rows = np.vstack((rows,np.array((28,36,36),dtype=np.float32)))#schwarz
    rows = np.vstack((rows,np.array((53, 150, 146),dtype=np.float32)))#hellgrau
    rows = np.vstack((rows,np.array(image[160,613],dtype=np.float32)))#dunkelgrau im Hintergrund
    rows = np.vstack((rows,np.array((162, 217, 255),dtype=np.float32)))#gelb auf Widerständen
    rows = np.vstack((rows,np.array((242, 249, 252),dtype=np.float32)))#weiß Platinenrand
    
    train = rows
    response= np.array([0,0,1,1,1,1,1]).astype(int) 
  
    svm.train(train, cv2.ml.ROW_SAMPLE, response)
    
    erg = svm.predict(image.reshape(height*width,3).astype(np.float32))
    erg= erg[1].reshape(height,width).astype(np.uint8)
    ergColor=np.zeros((height,width,3)).astype(np.uint8)
    #Farbbilderstellung
    ergColor[erg==1]=(0,0,0)
    ergColor[erg==0]=(255,255,0)
   
    result.append({"name":"ErgebnisSvmBunt","data":ergColor})

    #-----------------------Größte Kontur finden-- ---------------------------#
    imageGrey = cv2.cvtColor(np.copy(ergColor), cv2.COLOR_RGB2GRAY)
    _,thresh1 = cv2.threshold(imageGrey,80,255,cv2.THRESH_BINARY) 
    contours,_ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contoursgood = max(contours, key = cv2.contourArea)
    imageDrawnCont = cv2.drawContours(np.copy(image), contoursgood, -1, (0,255,0), 2)

    result.append({"name":"KonturenAufPcb","data":imageDrawnCont})

    #------------------Rechtech um größte Kontur legen------------------------#
    rect = cv2.minAreaRect(contoursgood)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    imageRect = cv2.drawContours(np.copy(image), [box], -1, (0,255,0), 2)
    result.append({"name":"RechteckUmPcb","data":imageRect})
    
    #--------------------------Rotation entfernen-----------------------------#
    center = rect[0]    
    angle = rect[2]     
    if angle > 45:
        angle = -90+angle
    scale = 1
    rotMat = cv2.getRotationMatrix2D(center,angle,scale)
    rotated_blob = cv2.warpAffine(image, rotMat, (width, height))

    result.append({"name": "rotated_blob","data": rotated_blob})
    #-------------------------Verschiebung entfernen-------------------------#
    shiftMat = np.array([1, 0, width/2-center[0], 0, 1, height/2-center[1]], dtype=np.float64).reshape(2, 3)
    shiftRot_blob = cv2.warpAffine(rotated_blob, shiftMat, (width, height))

    result.append({"name": "shiftedAndRotated_blob","data": shiftRot_blob})
    #------------------------PCB Bereich ausschneiden----------------------#
    #Seitenlängen des Ausschnitts anhand des generierten Rechtecks berechnen
    center = np.int0(center)
    a = box[0][0] - box[1][0]
    b = box[0][1] - box[1][1]
    shortSide = np.sqrt((a**2)+(b**2))
    c = box[1][0] - box[2][0]
    d = box[1][1] - box[2][1]
    longSide = np.sqrt((c**2)+(d**2))
    if shortSide > longSide:
         (longSide, shortSide) = (shortSide, longSide)
    shortSide = 1.05*shortSide
    longSide = 1.05*longSide
    #Da das Recheck nicht die Pins mit einschließt muss hier ein Korrekturwert festgelegt werden
    pinExtra = 150
    #Ausschnitt an der richtigen Stelle setzen (shiftRot_blob[erste Reihe:letzteReihe, erste Spalte:letzte Spalte])
    pcbCutout = shiftRot_blob[(int(height/2)-int(shortSide/2))-pinExtra:int(height/2)+int(shortSide/2),int(width/2)-int(longSide/2):int(width/2)+int(longSide/2)]

    result.append({"name":"PcbCoutout","data":pcbCutout})

if __name__ == '__main__':
    image=cv2.imread("..\Images\pcb2.JPG")
    result=[]
    run(image,result)
    for ele in result:
        cv2.imshow(ele["name"],ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()