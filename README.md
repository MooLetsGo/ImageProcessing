Dokumntation Bildverabeitung Gruppe: Konrad, Thesing, Gütermann

Bei der Abgabe sind kommentierte Vorgänger-Programme von uns dabei an denen man den Arbeitsverlauf beobachten Konturenanalyse

Zusammendassend:

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
Rotitaion und Verschiebung rausnehmen funktioniert
Da auf einigen Bildern die Pins nicht erkannt werden werden Grenzwerte für die Bildgröße bestimmt mit denen sich das aus der Kontur ergebende Bild angepasst wird

Probleme: einige Konturen noch unsauber wegen Erkennungsproblemen am Rand
Lösungsansatz: Fallunterscheidung für Erkennung mit Rand und ohne aghängig von der Konturgröße

Problem: Pins zeigen nach unten: wenn die Pins nach unten Zeigen und von der Konturanalyse nicht erkannt werden, steht das Bild auf dem Kopf da es nur nach oben an die Bildgröße angepasst wird.
Überlegung: Pins müssen irgendwie erkannt werden
