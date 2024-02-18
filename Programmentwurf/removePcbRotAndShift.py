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
    #svm.setKernel(cv2.ml.SVM_RBF)
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
    #ergColor=cv2.resize(ergColor,None,None,3,3,cv2.INTER_NEAREST
    erg = erg.reshape(height,width)/5.01

    result.append({"name":"ErgebnisSvm","data":erg})
    result.append({"name":"ErgebnisSvmBunt","data":ergColor})

    #-----------------------Konturen finden und Rechteck um PCB ---------------------------#

    imageGrey = cv2.cvtColor(np.copy(ergColor), cv2.COLOR_RGB2GRAY)
    _,thresh1 = cv2.threshold(imageGrey,80,255,cv2.THRESH_BINARY) 
    contours,_ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #contoursgood=[]*1
    #print(contoursgood)
    #maxArea = 0
    #for c in contours:
    #    if cv2.contourArea(c) > maxArea:
    #        contoursgood.append(c)
    #        maxArea = cv2.contourArea(c)
    contoursgood = max(contours, key = cv2.contourArea)
    imageDrawnCont = cv2.drawContours(np.copy(image), contoursgood, -1, (0,255,0), 2)
    result.append({"name":"KonturenAufPcb","data":imageDrawnCont})

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
    #shiftMat = cv2.matFromArray(2, 3, cv2.CV_64FC1, [1, 0, 128-center[0], 0, 1, 128-center[1]])
    shiftRot_blob = cv2.warpAffine(rotated_blob, shiftMat, (width, height))
    result.append({"name": "shiftedAndRotated_blob","data": shiftRot_blob})

    #---------------------Rechteck größer machen ------------------------------#
    #Kontur neu finden, um die neuen boxPunkte des Rechecks zu bekommen
    #rows = np.vstack((rows,np.array((0, 255,  0),dtype=np.float32)))#grünes kleines Rechteck

    erg2 = svm.predict(shiftRot_blob.reshape(height*width,3).astype(np.float32))
    erg2= erg2[1].reshape(height,width).astype(np.uint8)
    ergColor2=np.zeros((height,width,3)).astype(np.uint8)
    #Farbbilderstellung
    ergColor2[erg2==1]=(0,0,0)
    ergColor2[erg2==0]=(255,255,0)
    erg2 = erg2.reshape(height,width)/5.01
    result.append({"name":"Ergebnis2Svm","data":erg2})

    imageGrey2 = cv2.cvtColor(np.copy(ergColor2), cv2.COLOR_RGB2GRAY)
    _,thresh2 = cv2.threshold(imageGrey2,80,255,cv2.THRESH_BINARY) 
    contours2,_ = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #contoursgood2=[]
    #maxArea2 = 0
    #for c in contours2:
    #    if cv2.contourArea(c) > maxArea2:
    #        contoursgood2.append(c)
    #        maxArea2 = cv2.contourArea(c)
    contoursgood2 = max(contours2, key = cv2.contourArea)
    rect2 = cv2.minAreaRect(contoursgood2)
    box2 = cv2.boxPoints(rect2)
    box2 = np.int0(box2)

    ##Min1 und Min2 braucht man nur, da es bei manchen Bildern leichte Abweichungen im Y-Wert gibt (Rechteck nicht ganz gerade)
    #Y-Koordinaten der Eckpunkte extrahieren
    box2Y = np.copy(box2[:,1])
    #Ersten Minimalen Y Wert bestimmen
    i = 1
    for v in box2Y:
         if i == 1:
              min1 = v
              posMin1 = i-1
         elif v < min1:
              min1 = v
              posMin1 = i-1
         i += 1
    box2Y[posMin1] += 50
    #Zweiten minimalen Y Wert bestimmen
    i = 1
    for v in box2Y:
         if i == 1:
              min2 = v
         elif v < min2:
              min2 = v
         i += 1            

    #Die Minimalen Y Koordinaten um -150 verschieben (Rechteck nach oben strecken damit auch die Pins
    # mit eingeschlossen werden)
    for index1 in range(len(box2)):
         for index2 in range(len(box2[index1])):
              if box2[index1][index2] == min1 or box2[index1][index2] == min2:#Toleranz +- 
                   box2[index1][index2] -= 150      
     
     #Alternativer Ansatz von David
     #sumbox2 = []
     #for i in box2:
     #     sumbox2.append(i[0]+i[1])
    print(box2)
    imageRect2 = cv2.drawContours(np.copy(shiftRot_blob), [box2], -1, (0,255,0), 2)
    result.append({"name":"RechteckUmPcbGesamt","data":imageRect2})

    #------------------------PCB Bereich ausschneiden----------------------#
    #[[ 219  747]
     #[ 219  171]
     #[1184  172]
     #[1184  747]]

     
    
    