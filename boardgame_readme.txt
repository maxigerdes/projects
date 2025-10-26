Das Spiel Boardgame.py ist eine Konsolen Version von dem Spiel Dicke Luft in der Gruft. 

Ziel des Spiels ist es seine Farbkarten(Vampire) in ein Leeres Feld mit der selben Farbe zu legen.
Gewonnen hat der Spiler der als erstes keine Karten mehr hat.

Ein Spieler sieht immer nur die vier äußeren seiner Karten und darf nur die jeweils Äußere Karte auswählen.
Wenn ein Spieler 3 mal Feld aufgedeckt hat, welches schon belegt ist, dürfen alle anderen Spieler eine Karte abgeben. Diese Karten sieht man immer und dürfen immer benutzt werden.

Man hat auch die Option einen von 3 Knobläuche in ein Grab zu legen. Deckt jemand dieses Feld auf, darf ich diesem Spieler 2 meiner Karten abgeben. Decke ich das Feld auf, bekomme ich von allen Spielern eine Karte.

Es gibt noch 6 Sonderfelder, nämlich die Ratten. Decke ich dieses Feld auf, darf ich solange umliegende Felder aufdekcen, bis ich nicht mehr möchte, oder ein volles Grab aufdecke.

Bislang existiert nur diese Konsolen Version. Das Ziel ist langfristig eine Frontend Lösung dafür zu bauen. Deshalb ist die Input validation nur zu Teilen umgesetzt, da diese Später durch das UI eh vorgegeben sein wird.

Um ein Grab/Feld aufzudecken, muss der Spieler eine Koordinate in dem Format (x,y) zb 2,5 eingeben. Alle Optionen werden in Form einer Koordinaten Karte angezeigt.
Ein Knoblauch wird je nach Zug entweder mit "k" oder mit "j" gelegt. Das wird aber auch nochmal in der Konsole ausgegeben. 
Normale Farbkarten/Vampire werden abgelegt, indem ich aus einer der Verfügbaren_karten und Straf_karten auswähle. Diese sind mit nummern versehene. Durch eingabe dieser Nummer wird diese Karte abgelegt. 
Hier kann man theoretisch schummeln, da die Validierung ob man die Richtige Karte abgelegt hat nicht implementiert ist. Bitte Spielt ehrlich.

In der ergebnisse.csv werden die Siege pro Spieler dokumentiert.