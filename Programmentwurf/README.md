Im Ordner CutoutFunktionen liegen die Programme welche für die Erstellung des passenden PCB Bildausschnittes verwendet werden

Das generateTrainingdata Programm verwendet die aktuellste Cutout Funktion um einen Trainingsdatensatz aus den pcb2 Bildern zu erstellen
(Aktuell ist ein Schleifendurchlauf in der Hilfsfunktion "cutoutPcb" im "generateTrainingdata" Programm noch auf 30 limitiert -> Um einen Trainingsdatensatz aus allen Bildern zu erstellen eine der beiden "abgabe" Programme verwenden)

Anwendung des generateTrainingdata Programms:
1. Pfade an eigene Umgebung anpassen
2. Programm starten
3. Hoffen, dass alles funktioniert

In der ToDo.txt stehen Sachen die nicht funktionieren :(  

----------------------------------------------------------------

Ansonsten grobe Beschreibung Entwicklungsverlauf/ Dokumentation:

Dokumentation Bildverabeitung Gruppe: Konrad, Thesing, Gütermann

Bei der Abgabe sind kommentierte Vorgänger-Programme von uns dabei an denen man den Arbeitsverlauf beobachten kann

Zusammenfassend:

1.
Erstellung des Binärblid zur Konturenanalyse mit cv2.threshold
Filtern nach größter Kontur
Erstellung eines Rechtecks um Kontur der Paltine mit cv2.minAreaRect
Rotieren 

Probleme: nicht bei allen Bilder wurden die richtigen Konturen erfasst bzw. falsches Rechteck; Rotation zur falschen Seite
Lösungsansatz: Konturanalyse verbessern mit Kontrasrterhöhung oder SVM; Rotationswinkel angleichen

2.
Konturanalyse mit Kontrasterhöung eher semi erfolgreich
Rotationswinkel mit if angle > 45: angle -= 90 angleichen funktioniert

3.
Konturanalyse mit SVM funktioniert besser
Binärbild aus SVM wird direkt für die Konturanalyse verwendet d.h. keine threshold mehr
Rotitaion und Verschiebung rausnehmen funktioniert

Da auf einigen Bildern die Pins nicht erkannt werden, werden Grenzwerte für die Bildgröße bestimmt mit denen, sich das aus der Kontur ergebende Bild, angepasst wird

Probleme: einige Konturen noch unsauber wegen Erkennungsproblemen am Rand
Lösungsansatz: Fallunterscheidung für Erkennung mit Rand und ohne aghängig von der Konturgröße

Problem: Pins zeigen nach unten: wenn die Pins nach unten Zeigen und von der Konturanalyse nicht erkannt werden, steht das Bild auf dem Kopf da es nur nach oben an die Bildgröße angepasst wird.
Überlegung: Pins müssen irgendwie erkannt werden