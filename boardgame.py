import random
import pandas as pd
class player:
    def __init__ (self, name,spielernummer):
        self.name = name
        self.karten = []
        self.karten_strafe = []
        self.strafe = 0
        self.siege = 0
        self.spielernummer = spielernummer
        self.auswählbare_karten  = []
        self.knoblauch = 3

    def sichtbare_karten_berechnen (self):
        self.auswählbare_karten = []
        if len(self.karten) == 0:
            pass
        if len(self.karten) == 1:
            self.auswählbare_karten.append(self.karten[0])
        if len(self.karten) >= 2:
            self.auswählbare_karten.append(self.karten[0])
            self.auswählbare_karten.append(self.karten[-1])

        self.auswählbare_karten += self.karten_strafe

    def karten_abgeben(self,knoblauch=False):
        string = "Welche Karte möchtest du in das Grab legen? (1,2,...): "

        if self.knoblauch > 0:
                string = "Welche Karte möchtest du in das Grab legen? (1,2,...). Du hast außerdem noch einen Knoblauch, den du einsetzten kannst (gib 'k' ein): "
        print(string)
        eingabe = input()
        if eingabe == 'k':
            self.knoblauch -= 1
            print("Du hast deinen Knoblauch eingesetzt")
            return 'knoblauch'
        else :
            eingabe = int(eingabe)
        
        if eingabe == 1:
            karte = self.karten.pop(0)
            print(f"Du hast die Karte {karte} abgegeben.")

        if eingabe == 2:
            karte = self.karten.pop(-1)
            print(f"Du hast die Karte {karte} abgegeben.")

        if eingabe >= 3 and eingabe < len(self.karten)+3:
            karte = self.karten_strafe.pop(eingabe-3)
            print(f"Du hast die Karte {karte} abgegeben.")
        return 'besetzt'

    def karten_print (self):

        print("Deine Karten sind:")
        print("")
        sichtbare_karten = ["?" for _ in self.karten]
        if len(self.karten) == 0:
            sichtbare_karten = []
            print(sichtbare_karten)
        if len(self.karten) == 1:
            sichtbare_karten[0] = self.karten[0]
            print(sichtbare_karten)
            print("1:", self.karten[0])
        if len(self.karten) == 2:
            sichtbare_karten[0] = self.karten[0]
            sichtbare_karten[1] = self.karten[1]
            print(sichtbare_karten)
            print(f"1: {self.karten[0]}, 2: {self.karten[-1]}")
        if len(self.karten) == 3:
            sichtbare_karten[0] = self.karten[0]
            sichtbare_karten[1] = self.karten[1]
            sichtbare_karten[2] = self.karten[2]
            print(sichtbare_karten)
            print(f"1: {self.karten[0]}, 2: {self.karten[-1]}")
        if len(self.karten) >= 4:
            sichtbare_karten[0] = self.karten[0]
            sichtbare_karten[1] = self.karten[1]
            sichtbare_karten[-2] = self.karten[-2]
            sichtbare_karten[-1] = self.karten[-1]
            print(sichtbare_karten)
            print(f"1: {self.karten[0]}, 2: {self.karten[-1]}")
        print("")
        print("Deine Strafekarten sind:")
        print(self.karten_strafe)
        string = ""
        if len(self.karten_strafe) != 0:
            for i in range(len(self.karten_strafe)):
                string += f"{i+3}:{self.karten_strafe[i]} "
        print(string)
        print("")
        self.sichtbare_karten_berechnen()

    def anzahl_karten (self):
        return len(self.karten) + len(self.karten_strafe)

class spielfeld:
    
    def __init__ (self):
        self.gräber = [[None for _ in range(4)] for _ in range(15)]
        self.gräber_status = [["leer" for _ in range(4)] for _ in range(15)]
        self.koordinaten = [[None for _ in range(4)] for _ in range(15)]
    
    def koordinaten_befüllen (self):
        for row in range(15):
            for col in range(4):
                self.koordinaten[row][col] = (row+1, col+1)
        return self.koordinaten
    
    def koordinaten_print (self):
        for row in self.koordinaten:
            print (row)

    def gräber_befüllen (self,karten):
        for row in range(15):
            for col in range(4):
                self.gräber[row][col] = karten.pop()
        return self.gräber
    
    def gräber_print (self):
        for row in self.gräber:
            print (row)

class game:

    def __init__ (self):
        self.spieler_liste = []
        self.anzahl_spieler = 0
        self.spielfeld = None
        self.ratten_karten = []
        self.turn = 0
        self.stop_play = False
        self.save_data = True

    def play_turn (self):
        print("Nächster Zug für Spieler", self.spieler_liste[self.turn].name)
        print("Zum fortfahren drücke Enter")
        input()
        self.spieler_liste[self.turn].karten_print()
        self.spielfeld.koordinaten_print()
        karte, status,reihe, spalte = self.feld_aufdecken()
        modus = self.check_status(status,karte)
        self.modus(modus,reihe, spalte,karte)
        print("Dein Zug ist zuende! Zum Fortfahren drücke Enter")
        input()

    def feld_aufdecken(self):
        print("Welches Feld möchtest du aufdecken?")
        input_koordinate = input("Gib die Koordinate im Format 'Reihe,Spalte' ein: ")
        if input_koordinate == "ende":
            return None, 'ende', None, None
        try:
            reihe, spalte = map(int, input_koordinate.split(','))
            if 1 <= reihe <= 15 and 1 <= spalte <= 4:
                karte = self.spielfeld.gräber[reihe - 1][spalte - 1]
                status = self.spielfeld.gräber_status[reihe - 1][spalte - 1]
                return karte, status, reihe, spalte
            else:
                print("Ungültige Koordinate. Bitte versuche es erneut.")
                self.feld_aufdecken()
        except ValueError:
            print("Ungültiges Format. Bitte gib die Koordinate im Format 'Reihe,Spalte' ein.")
            self.feld_aufdecken()

    def check_status(self,status,karte):
        print(f"Du hast ein Grab mit der Farbe {karte} aufgedeckt:")
        if karte != "ratte":
            if status == "leer":
                print("Das Grab ist leer.")
                return "leer"
            if status == "besetzt":  
                print("In deinem Grab liegt bereits eine Karte. Du bekommst einen Pflock.")
                self.spieler_liste[self.turn].strafe += 1
                return "besetzt"
            if status == self.turn:
                print("Du hast deinen eignenen Knoblauch aufgedeckt. Alle spieler dürfen die eine Karte abgeben")
                return status
            if status in range(self.anzahl_spieler) and status != self.turn:
                print(f"Du hast den Knoblauch von Spieler {self.spieler_liste[status].name} aufgedeckt. Dieser Spieler darf dir nun zwei Karten abgeben.")
                return status
        else:
            print("Du hast eine Ratte aufgedeckt!")
            return "ratte"

    def modus(self,modus,reihe, spalte,karte,ratte=False):
        if modus == "leer":
            self.leer(reihe, spalte,ratte)
        elif modus == "besetzt":
            self.besetzt()
        elif modus == "ratte":
            self.ratte(reihe, spalte,karte)
        elif modus == self.turn:
            self.eigener_knoblauch(reihe, spalte)
        else:
            self.fremder_knoblauch(modus, reihe, spalte)

    def eigener_knoblauch(self,reihe, spalte):
        self.spieler_liste[self.turn].knoblauch += 1
        self.spielfeld.gräber_status[reihe - 1][spalte - 1] = 'leer'
        for spieler in self.spieler_liste:
            if spieler != self.spieler_liste[self.turn]:
                print(f"Spieler {spieler.name}, Karte möchtest du abgeben?")
                spieler.karten_print()
                strafkarte = self.karte_abgeben(spieler)
                self.spieler_liste[self.turn].karten_strafe.append(strafkarte)
                if self.spielende() == True:
                    break
        self.turn = (self.turn + 1) % self.anzahl_spieler

    def fremder_knoblauch(self,modus,reihe, spalte):   
        self.spieler_liste[modus].knoblauch += 1
        self.spielfeld.gräber_status[reihe - 1][spalte - 1] = 'leer'
        print(f"Spieler {self.spieler_liste[modus].name}, welche zwei Karten möchtest du abgeben?")
        for _ in range(2):
            self.spieler_liste[modus].karten_print()
            strafkarte = self.karte_abgeben(self.spieler_liste[modus])
            self.spieler_liste[self.turn].karten_strafe.append(strafkarte)
            if self.spielende() == True:
                break 
        self.turn = (self.turn + 1) % self.anzahl_spieler

    def ratte(self,reihe, spalte,karte):
        reihe = reihe
        spalte = spalte 
        karte = karte

        print("Das heißt, du darfst so lange die umliegenden Gräber aufdecken, bis du nicht mehr möchtest, oder kein leeres Grab mehr findest. Das Rattenfeld wird hinterher durch eine neue Karte ersetzt")
        ausgabe = [
        [[reihe-1, spalte-1], [reihe-1, spalte], [reihe-1, spalte+1]],
        [[reihe, spalte-1], ["Ratte"], [reihe, spalte+1]],
        [[reihe+1, spalte-1], [reihe+1, spalte], [reihe+1, spalte+1]]
        ]
        #ausgabe felder löschen, falls die ratte am rand lag
        for i in range(3):
            for j in range(3):
                if ausgabe[i][j] != ["Ratte"]:
                    if ausgabe[i][j][0] < 1 or ausgabe[i][j][0] > 15 or ausgabe[i][j][1] < 1 or ausgabe[i][j][1] > 4:
                        ausgabe[i][j] = "X"
        print(ausgabe)
        turn = self.turn
        self.spielfeld.gräber[reihe - 1][spalte - 1] = self.ratten_karten.pop()
        while self.turn == turn:
            if self.spielende() == True:
                break
            print("Welches Feld möchtest du aufdecken? (Gib 'ende' ein, um aufzuhören)")
            karte_2,Status_2,x_koordinate,y_koordinate = self.feld_aufdecken()
            if Status_2 == "ende":
                print("Du hast die Rattenrunde beendet.")
                self.turn = (self.turn + 1) % self.anzahl_spieler
            else:
                ratte = True
                modus = self.check_status(Status_2,karte_2)
                self.modus(modus,x_koordinate,y_koordinate,karte_2,ratte)
            

    def spielende(self):
        for i in range(len(self.spieler_liste)):
            if self.spieler_liste[i].anzahl_karten() == 0:
                self.stop_play = True
        return self.stop_play

    def besetzt(self):
        if self.spieler_liste[self.turn].strafe >= 3:
            print("Du hast 3 Pflöcke! Alle anderen Spieler dürfen dir eine Karte abgeben.")
            for spieler in self.spieler_liste:
                if spieler != self.spieler_liste[self.turn]:
                   print(f"Spieler {spieler.name}, welche Karte möchtest du abgeben?")
                   spieler.karten_print()
                   strafkarte = self.karte_abgeben(spieler)
                   self.spieler_liste[self.turn].karten_strafe.append(strafkarte)
                   if self.spielende() == True:
                       break 
            self.spieler_liste[self.turn].strafe = 0
        else:
            pass
        self.turn = (self.turn + 1) % self.anzahl_spieler
        return 1


    def karte_abgeben(self,spieler):
        eingabe = int(input())
        if eingabe == 1:
            karte = spieler.karten.pop(0)
            print(f"Du hast die Karte {karte} abgegeben.")
        elif eingabe == 2:
            karte = spieler.karten.pop(-1)
            print(f"Du hast die Karte {karte} abgegeben.")
        elif eingabe >= 3 and eingabe < len(spieler.karten)+3:
            karte = spieler.karten_strafe.pop(eingabe-3)
            print(f"Du hast die Karte {karte} abgegeben.")
        return karte

    def leer(self,reihe, spalte,ratte=False):
        self.spieler_liste[self.turn].karten_print()
        grab =  self.spielfeld.gräber[reihe - 1][spalte - 1]
        if grab in self.spieler_liste[self.turn].auswählbare_karten:
            status = self.spieler_liste[self.turn].karten_abgeben()
            if status == 'knoblauch':
                self.turn = (self.turn + 1) % self.anzahl_spieler
                self.spielfeld.gräber_status[reihe - 1][spalte - 1] = self.turn
                return None 
            if status == 'besetzt':
                self.spielfeld.gräber_status[reihe - 1][spalte - 1] = status
            if ratte == False:
                print("Super! Da du eine Karte abgelegt hast, darfst du noch einen Zug machen.")
            if ratte == True:
                print("Super! Da du eine Karte abgelegt hast, darfst du noch ein Grab aufdecken.")
        else:
            print("Du hast keine passende Karte.")
            if self.spieler_liste[self.turn].knoblauch > 0:
                print("Möchtest du einen Knoblauch einsetzen? Bestätige mit (j/n)")
                eingabe = input()
                if eingabe == 'j':
                    self.spieler_liste[self.turn].knoblauch -= 1
                    print("Du hast deinen Knoblauch eingesetzt")
                    self.spielfeld.gräber_status[reihe - 1][spalte - 1] = self.turn
                    self.turn = (self.turn + 1) % self.anzahl_spieler
                    return None
                else:
                    if ratte == False:
                        print("Du hast keine passende Karte.")
                        self.turn = (self.turn + 1) % self.anzahl_spieler
                    if ratte == True:
                        print("Du hast keine passende Karte. Probiere ein anderes Grab.")   

    def gamestart(self):
        self.spieler_einlesen()
        self.spielfeld_erstellen()
        self.karten_verteilen()

    def spieler_einlesen(self):

        
        print("Willkommen bei Dicke Luft in der Gruft!")
        print("")
        print("Wie viele Spieler nehmen teil? Bitte Zahl zwischen 2 und 6 Eingeben:")
        while True:
            try:
                self.anzahl_spieler = int(input())
                if self.anzahl_spieler not in (2, 3, 4, 5, 6):
                    print(" Falsche Eingabe. Bitte eine Zahl zwischen 2 und 6 eingeben.")
                    continue
                    
                else:
                    print("Danke! Es nehmen", self.anzahl_spieler, "Spieler teil.")

            except ValueError:
                print("Ungültige Eingabe. Bitte eine Zahl zwischen 2 und 6 eingeben.")
                continue
            break

        print("Bitte geben sie die Namen der Spieler ein:")
        for i in range(self.anzahl_spieler):
            print("Wie ist der Name von Spieler", i+1, "?")
            name = input()
            spieler = player(name,spielernummer=i+1)
            self.spieler_liste.append(spieler)

        print("Die Spieler sind:")
        for spieler in self.spieler_liste:
            print(spieler.name)
        print("Drücke Enter, um das Spiel zu starten.")
        input()

    def spielfeld_erstellen(self):
        self.spielfeld = spielfeld()
        self.spielfeld.koordinaten_befüllen()
        farben = ["rot", "blau", "gelb", "grün", "schwarz", "weiß"]
        karten = farben * 10
        random.shuffle(karten)
        self.ratten_karten = karten[-6:]
        ratten = ["ratte" for _ in range(6)]
        karten = karten[:-6] + ratten
        random.shuffle(karten)
        self.spielfeld.gräber_befüllen(karten)

    def karten_verteilen(self):
        #karten_pro_spieler = 60/self.anzahl_spieler
        #farben = ["rot", "blau", "gelb", "grün", "schwarz", "weiß"]
        #karten = farben * 10
        karten = ["rot","blau"]
        karten_pro_spieler = len(karten)/self.anzahl_spieler
        random.shuffle(karten)
        for spieler in self.spieler_liste:
            for _ in range(int(karten_pro_spieler)):
                karte = karten.pop()
                spieler.karten.append(karte)

    def ergebniss_speichern(self):
        #csv mit spilernamen und anzahl siege updaten
        df = pd.read_csv('ergebnisse.csv')
        for player in self.spieler_liste:
            if player.name in df['Name'].values:
                df.loc[df['Name'] == player.name, 'Siege'] += player.siege
            else:
                new_row = {'Name': player.name, 'Siege': player.siege}
                df = df.append(new_row, ignore_index=True)
        df.to_csv('ergebnisse.csv', index=False)


    def engine(self):
        print("Das Spiel beginnt!")
        while self.stop_play == False:
            self.play_turn()
            self.spielende()
        for player in self.spieler_liste:
            if player.anzahl_karten() == 0:
                print("Hurra ! Spieler", self.spieler_liste[self.turn].name, "hat gewonnen!")
                print("Das Spiel ist zuende.")
                self.spieler_liste[self.turn].siege += 1
        self.ergebniss_speichern()
        print("Danke fürs Spielen!")


if __name__ ==  '__main__':

    spiel = game()
    #spiel.load_game()
    spiel.gamestart()
    spiel.engine()
    #spiel.save_game()
