import os
import numpy as np
import cv2
import random
import shutil

#--------------------Hilfsfunktionen--------------------#

def cutoutPcb(image,settings=(2,50)):

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
    #rows = np.vstack((rows,np.array((255, 255,  254),dtype=np.float32)))#weiß Platinenbeschriftung

    rows = np.vstack((rows,np.array((28,36,36),dtype=np.float32)))#schwarz
    rows = np.vstack((rows,np.array((53, 150, 146),dtype=np.float32)))#hellgrau
    rows = np.vstack((rows,np.array(image[160,613],dtype=np.float32)))#dunkelgrau im Hintergrund
    rows = np.vstack((rows,np.array((162, 217, 255),dtype=np.float32)))#gelb auf Widerständen
    rows = np.vstack((rows,np.array((242, 249, 252),dtype=np.float32)))#weiß Platinenrand
    
    train = rows
    response= np.array([1,1,0,0,0,0,0]).astype(int) 
  
    svm.train(train, cv2.ml.ROW_SAMPLE, response)
    
    erg = svm.predict(image.reshape(height*width,3).astype(np.float32))
    erg= erg[1].reshape(height,width).astype(np.uint8)

    #-----------------------Größte Kontur finden-- ---------------------------#
    contours,_ = cv2.findContours(erg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contoursgood = max(contours, key = cv2.contourArea)
    imageDrawnCont = cv2.drawContours(np.copy(image), contoursgood, -1, (0,255,0), 2)

    

    #------------------Rechtech um größte Kontur legen------------------------#
    rect = cv2.minAreaRect(contoursgood)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    imageRect = cv2.drawContours(np.copy(image), [box], -1, (0,255,0), 2)
    
    
    #--------------------------Rotation entfernen-----------------------------#
    center = rect[0]    
    angle = rect[2]     
    if angle > 45:
        angle = -90+angle
    scale = 1
    rotMat = cv2.getRotationMatrix2D(center,angle,scale)
    rotated_blob = cv2.warpAffine(image, rotMat, (width, height))

    
    #-------------------------Verschiebung entfernen-------------------------#
    shiftMat = np.array([1, 0, width/2-center[0], 0, 1, height/2-center[1]], dtype=np.float64).reshape(2, 3)
    shiftRot_blob = cv2.warpAffine(rotated_blob, shiftMat, (width, height))

    #------------------------PCB Bereich ausschneiden----------------------#
    #Seitenlängen des Ausschnitts anhand des generierten Rechtecks berechnen
    shortSide = rect[1][0]
    longSide = rect[1][1]
    if shortSide > longSide:
         (longSide, shortSide) = (shortSide, longSide)

    #Eventuelle anpassung der Seitenlängen, da die generierten Rechtecke nicht bei jedem Bild gleich sind
    shortSide = 1.05*shortSide
    longSide = 1.02*longSide
         
    #Da das Recheck nicht die Pins mit einschließt muss hier ein Korrekturwert festgelegt werden
    maxShortSide = 580 #580 wurde durch ausprobieren ermittelt -> Länge shortSide von einem Recheck das gut an die Kontur des PCB passt; pi mal Daumen 150 draufaddiert -> 580 war das Ergebnis
    pinExtra = int(maxShortSide - shortSide)
    #Ausschnitt an der richtigen Stelle setzen (shiftRot_blob[erste Reihe:letzteReihe, erste Spalte:letzte Spalte])
    src = shiftRot_blob[(int(height/2)-int(shortSide/2))-pinExtra:int(height/2)+int(shortSide/2),int(width/2)-int(longSide/2):int(width/2)+int(longSide/2)]
    #Resize, damit alle Ausschnitte die gleiche Größe haben; Eigentlich kann man dann den Ausschnitt auch gleich hartkodieren -> die 1010 und 580 sind halt Werte, die einmal
    #berechnet wurden aber dann eigentlich für alle Bilder angewendet werden können
    pcbCutout = cv2.resize(src,(1010,580),interpolation=cv2.INTER_NEAREST)
    return pcbCutout
    
def saveFiles(srcPath,dstPath):
    i = 0
    files = os.listdir(srcPath)
    for file in files:
        pcbCutout = cutoutPcb(image=cv2.imread(srcPath+'/'+file))
        bildpfad=dstPath+'/'+str(file).split('.')[0]+'.png'
        cv2.imwrite(bildpfad, pcbCutout)
        i += 1
        if i == 30:
            break
    return

def randomTen(list):
    #Anzahl der Elemente, die ausgewählt und entfernt werden sollen (10% der Gesamtanzahl)
    anzahlZuEntfernen = int(len(list) * 0.1)
    #Zufällige Auswahl von 10% der Elemente
    ausgewaehlteElemente = random.sample(list, anzahlZuEntfernen)
    
    return ausgewaehlteElemente
            
def generateTrainingdata(srcPathNormal,srcPathAnnormal,lernPathNormal,lernPathAnnormal,testPath):
    #Lernbilder "Normal" generieren
    
    
    saveFiles(srcPathNormal,lernPathNormal)

    #Lernbilder "Annormal generieren"
    
    
    saveFiles(srcPathAnnormal,lernPathAnnormal)

    #Liste mit zufälligen 10% aus Normal und Annormal erstellen
    imagesNormal = os.listdir(lernPathNormal)
    imagesAnnormal = os.listdir(lernPathAnnormal)

    randomTenNormal = randomTen(imagesNormal)
    randomTenAnnormal = randomTen(imagesAnnormal)

    #Elemente aus der Zufallsliste in aus Normal bzw. Annormal in Testen verschieben
    dst = testPath
    for ele in randomTenNormal:
        source = lernPathNormal +'/'+ ele
        destination = dst +'/'+ ele
        shutil.move(source,destination) #Datei verschieben

    for ele in randomTenAnnormal:
        source = lernPathAnnormal +'/'+ ele
        destination = dst +'/'+ ele
        shutil.move(source,destination) #Datei verschieben
    
    return


#--------------------Hauptprogramm---------------------#

#Dateipfade der Ordner angeben, in denen die Originalen (Normal, Annormal) Bilder des pcb2 Datensatzen liegen 
srcPathNormal = "C:/Users/morit/OneDrive/Studium/6_Semester/Digitale Bildverarbeitung/VisA_20220922/pcb2/Data/Images/Normal"
srcPathAnnormal = "C:/Users/morit/OneDrive/Studium/6_Semester/Digitale Bildverarbeitung/VisA_20220922/pcb2/Data/Images/Anomaly"

#Dateipfade der Ordner angeben, in denen die Bilder zum Lernen (Normal, Annormal) abgelegt werden sollen
lernPathNormal = "C:/Users/morit/OneDrive/Studium/6_Semester/Digitale Bildverarbeitung/ImageProcessing/Programmentwurf/Lernen/Normal"
lernPathAnnormal = "C:/Users/morit/OneDrive/Studium/6_Semester/Digitale Bildverarbeitung/ImageProcessing/Programmentwurf/Lernen/Annormal"

#Dateipfad des Ordners angeben, in dem die zufällig ausgewählten Testdaten abgelegt werden sollen
testPath = "C:/Users/morit/OneDrive/Studium/6_Semester/Digitale Bildverarbeitung/ImageProcessing/Programmentwurf/Testen"

#Funktionsaufruf um den pcb2 Datensatz für ein KI Training zu erstellen 
generateTrainingdata(srcPathNormal,srcPathAnnormal,lernPathNormal,lernPathAnnormal,testPath)
