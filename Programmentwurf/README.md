# CutoutFunktionen

Im Ordner "CutoutFunktionen" liegen die Programme, die zur Erstellung des passenden PCB-Bildausschnitts verwendet werden.

Das Programm "generateTrainingdata" nutzt die aktuellste Cutout-Funktion, um einen Trainingsdatensatz aus den "pcb2"-Bildern zu erstellen. Aktuell ist ein Schleifendurchlauf in der Hilfsfunktion "cutoutPcb" im Programm "generateTrainingdata" noch auf 30 limitiert. Um einen Trainingsdatensatz aus allen Bildern zu erstellen, verwenden Sie eines der "abgabe"-Programme.

## Anwendung des "generateTrainingdata" Programms:

1. Pfade an die eigene Umgebung anpassen.
2. Programm starten.
3. Hoffen, dass alles funktioniert.

In der "ToDo.txt" stehen Punkte, die noch nicht funktionieren.

### Grobe Beschreibung des Entwicklungsverlaufs / Dokumentation:

Dokumentation Bildverarbeitung Gruppe: Konrad, Thesing, Gütermann

Bei der Abgabe sind kommentierte Vorgänger-Programme enthalten, an denen der Arbeitsverlauf beobachtet werden kann.

#### Zusammenfassend:

- Erstellung des Binärbilds zur Konturenanalyse mit "cv2.threshold".
- Filtern nach größter Kontur.
- Erstellung eines Rechtecks um die Kontur der Platine mit "cv2.minAreaRect".
- Rotieren.

#### Probleme:

- Nicht bei allen Bildern wurden die richtigen Konturen erfasst bzw. das falsche Rechteck.
- Rotation zur falschen Seite.

#### Lösungsansätze:

- Konturanalyse verbessern mit Kontrasterhöhung oder SVM.
- Rotationswinkel angleichen.

#### Weiterentwicklung:

- Konturanalyse mit Kontrasterhöhung eher semi-erfolgreich.
- Rotationswinkel mit `if angle > 45: angle -= 90` angleichen funktioniert.
- Konturanalyse mit SVM funktioniert besser.
- Binärbild aus SVM wird direkt für die Konturanalyse verwendet, d.h. keine threshold mehr.
- Rotation und Verschiebung rausnehmen funktioniert.

#### Weitere Probleme und Lösungsansätze:

- Da auf einigen Bildern die Pins nicht erkannt werden, werden Grenzwerte für die Bildgröße bestimmt, mit denen sich das aus der Kontur ergebende Bild angepasst wird.
- Einige Konturen sind noch unsauber wegen Erkennungsproblemen am Rand.
- Fallunterscheidung für Erkennung mit Rand und ohne abhängig von der Konturgröße.
- Pins zeigen nach unten: Wenn die Pins nach unten zeigen und von der Konturanalyse nicht erkannt werden, steht das Bild auf dem Kopf, da es nur nach oben an die Bildgröße angepasst wird. Überlegung: Pins müssen irgendwie erkannt werden.
