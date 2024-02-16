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
    contoursgood=[]
    for c in contours:
        if cv2.contourArea(c) > 250000:
            contoursgood.append(c)
    imageDrawnCont = cv2.drawContours(np.copy(image), contoursgood, -1, (0,255,0), 2)
    result.append({"name":"KonturenAufPcb","data":imageDrawnCont})

    rect = cv2.minAreaRect(contoursgood[0])
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
    Mat = cv2.getRotationMatrix2D(center,angle,scale)
    rotated_blob = cv2.warpAffine(imageRect, Mat, (width, height))

    result.append({"name": "rotated_blob","data": rotated_blob})
