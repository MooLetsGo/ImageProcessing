import os
import numpy as np
import cv2
import random
import shutil

def cutoutPcb(image,settings=(2,50)):

    if(len(image.shape)!=3):
            print("Nur für Farbbilder")
            return
    height, width, *_ = image.shape[:]

    svm = cv2.ml.SVM_create()
    svm.setKernel(cv2.ml.SVM_LINEAR)
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setC(settings[0]/10+0.1)
    svm.setGamma(settings[0]/10.0+0.1)

    rows=np.array((154, 101,  10),dtype=np.float32)
    rows = np.vstack((rows,np.array((73, 42,  9),dtype=np.float32)))
    
    
    rows = np.vstack((rows,np.array((28,36,36),dtype=np.float32)))
    rows = np.vstack((rows,np.array((53, 150, 146),dtype=np.float32)))
    rows = np.vstack((rows,np.array(image[160,613],dtype=np.float32)))
    rows = np.vstack((rows,np.array((162, 217, 255),dtype=np.float32)))
    rows = np.vstack((rows,np.array((242, 249, 252),dtype=np.float32)))
    
    train = rows
    response= np.array([1,1,0,0,0,0,0]).astype(int) 

    svm.train(train, cv2.ml.ROW_SAMPLE, response)
    
    erg = svm.predict(image.reshape(height*width,3).astype(np.float32))
    erg= erg[1].reshape(height,width).astype(np.uint8)

    contours,_ = cv2.findContours(erg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contoursgood = max(contours, key = cv2.contourArea)
    
    rect = cv2.minAreaRect(contoursgood)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    center = rect[0]    
    angle = rect[2]     
    if angle > 45:
        angle = -90+angle
    scale = 1
    rotMat = cv2.getRotationMatrix2D(center,angle,scale)
    rotated_img = cv2.warpAffine(image, rotMat, (width, height))

    shiftMat = np.array([1, 0, width/2-center[0], 0, 1, height/2-center[1]], dtype=np.float64).reshape(2, 3)
    shiftedRotated_img = cv2.warpAffine(rotated_img, shiftMat, (width, height))

    shortSide = rect[1][0]
    longSide = rect[1][1]
    if shortSide > longSide:
         (longSide, shortSide) = (shortSide, longSide)

    shortSide = 1.05*shortSide
    longSide = 1.02*longSide
   
    maxShortSide = 580
    pinExtra = int(maxShortSide - shortSide)

    src = shiftedRotated_img[(int(height/2)-int(shortSide/2))-pinExtra:int(height/2)+int(shortSide/2),int(width/2)-int(longSide/2):int(width/2)+int(longSide/2)]
    pcbCutout = cv2.resize(src,(1010,580),interpolation=cv2.INTER_NEAREST)

    return pcbCutout
    
def saveFiles(srcPath,dstPath):

    files = os.listdir(srcPath)
    for file in files:
        pcbCutout = cutoutPcb(image=cv2.imread(srcPath+'/'+file))
        bildpfad=dstPath+'/'+str(file).split('.')[0]+'.png'
        cv2.imwrite(bildpfad, pcbCutout)

    return

def randomTen(list):

    anzahl = int(len(list) * 0.1)
    ausgewaehlteElemente = random.sample(list, anzahl)

    return ausgewaehlteElemente
            
def generateTrainingdata(srcPathNormal,srcPathAnnormal,lernPathNormal,lernPathAnnormal,testPath):

    saveFiles(srcPathNormal,lernPathNormal)

    saveFiles(srcPathAnnormal,lernPathAnnormal)

    imagesNormal = os.listdir(lernPathNormal)
    imagesAnnormal = os.listdir(lernPathAnnormal)

    randomTenNormal = randomTen(imagesNormal)
    randomTenAnnormal = randomTen(imagesAnnormal)

    dst = testPath
    for ele in randomTenNormal:
        source = lernPathNormal +'/'+ ele
        destination = dst +'/'+ ele
        shutil.move(source,destination)

    for ele in randomTenAnnormal:
        source = lernPathAnnormal +'/'+ ele
        destination = dst +'/'+ ele
        shutil.move(source,destination)
    
    return

#Dateipfade der Ordner angeben, in denen die Originalen (Normal, Annormal) Bilder des pcb2 Datensatzen liegen 
srcPathNormal = ""
srcPathAnnormal = ""

#Dateipfade der Ordner angeben, in denen die Bilder zum Lernen (Normal, Annormal) abgelegt werden sollen
lernPathNormal = ""
lernPathAnnormal = ""

#Dateipfad des Ordners angeben, in dem die zufällig ausgewählten Testdaten abgelegt werden sollen
testPath = ""

generateTrainingdata(srcPathNormal,srcPathAnnormal,lernPathNormal,lernPathAnnormal,testPath)
