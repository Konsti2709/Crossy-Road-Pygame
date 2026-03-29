import pygame
import random
from autos import Auto

SPIELFELD_BREITE = 20
SPIELFELD_HOEHE = 20

gras = "green"
strasse = "gray"
wasser = "lightblue"

BODEN = [gras, strasse, wasser]

strasse_richtungen = {}
strasse_timer = {}
strasse_intervalle = {}
spielfeld_map = []

y_verschiebung = 0

# Spielfeld generieren
def generieren(FENSTER, QUADRAT_HOEHE, QUADRAT_BREITE, autos, spieler):      
    FENSTER.fill("black")

    # Farbe festlegen und zeichnen
    for zeile in range(SPIELFELD_HOEHE):
        feld = spielfeld_map[zeile]

        if feld == gras:
            farbe = gras

        elif feld == strasse:
            farbe = strasse
        
        elif feld == wasser:
            farbe = wasser

        # links oben x, links oben y, breite, höhe
        quadrat = pygame.Rect(0, zeile * QUADRAT_HOEHE, SPIELFELD_BREITE * QUADRAT_BREITE, QUADRAT_HOEHE)

        # fenster, farbe, objekt
        pygame.draw.rect(FENSTER, farbe, quadrat)
    
    # Autopositionen durchgehen
    for auto in autos:
        # Auto erstellen
        quadrat = pygame.Rect(auto.x, auto.y + y_verschiebung, auto.breite, auto.hoehe)

        # Auto zeichnen 
        pygame.draw.rect(FENSTER, "blue", quadrat)  

    # Spieler erstellen
    quadrat = pygame.Rect(spieler.x, spieler.y, spieler.breite, spieler.hoehe)

    # Spieler zeichnen
    pygame.draw.rect(FENSTER, "red", quadrat)
    

def neu_generieren(FENSTER, QUADRAT_HOEHE, QUADRAT_BREITE, autos):
    for zeile in range(SPIELFELD_HOEHE):
        
        # Farbe und Feld festlegen
        if zeile >= 10:
            feld = gras
        else:
            feld = random.choice(BODEN)
        if feld == gras:
            farbe = gras
        elif feld == strasse:
            farbe = strasse
        elif feld == wasser:
            farbe = wasser

        # links oben x, links oben y, breite, höhe
        quadrat = pygame.Rect(0, zeile * QUADRAT_HOEHE, SPIELFELD_BREITE, QUADRAT_HOEHE)
        # fenster, farbe, objekt

        pygame.draw.rect(FENSTER, farbe, quadrat)

        # Spielfeld in Liste speichern
        spielfeld_map.append(feld)

    # Für jede Strasse Autos und Intervalle festlegen
    for zeile in range(len(spielfeld_map)):
        if spielfeld_map[zeile] == strasse:
            strasse_befüllen(zeile, QUADRAT_BREITE, QUADRAT_HOEHE, autos)
            intervall_festlegen(zeile)


def strasse_befüllen(zeile, QUADRAT_BREITE, QUADRAT_HOEHE, autos):
    # Random Anzahl Autos und Richtung
    anzahl_autos = random.randint(4, 6)
    richtung = random.choice([-1, 1])
    autos_in_der_zeile = []

    # Autos setzen
    for auto in range(anzahl_autos):
        

        max_versuche = 20

        auto_y = zeile * QUADRAT_HOEHE + QUADRAT_HOEHE / 10 - y_verschiebung

        for _ in range(max_versuche):
            auto_x = random.randint(0, SPIELFELD_BREITE) * QUADRAT_BREITE + QUADRAT_BREITE / 10
            neues_auto = Auto(auto_x, auto_y, richtung)

            neues_rechteck = pygame.Rect(neues_auto.x, neues_auto.y, neues_auto.breite, neues_auto.hoehe)

            kollidiert = False

            for anderes_auto in autos_in_der_zeile:
                anderes_rechteck = pygame.Rect(anderes_auto.x, anderes_auto.y, anderes_auto.breite, anderes_auto.hoehe)

                if neues_rechteck.colliderect(anderes_rechteck):
                      kollidiert = True
                      break
                
            if not kollidiert:
                autos_in_der_zeile.append(neues_auto)
                autos.append(neues_auto)
                break
        

    # Richtung der Strasse speichern für spätere Autos
    strasse_richtungen[zeile] = richtung


def intervall_festlegen(zeile):
    # Random Intervall für Auto-Spawnen festlegen
    intervall = random.randint(50, 200)

    # Intervalle und Timer speichern
    strasse_intervalle[zeile] = intervall
    strasse_timer[zeile] = intervall


def timer_runterzaehlen(zeile):
    # Jeden Frame Timer runterzählen
    strasse_timer[zeile] -= 1

    if strasse_timer[zeile] <= 0:
        # Neues Intervall festlegen
        intervall_festlegen(zeile)
        return True
    
    return False


def auto_spawnen(QUADRAT_BREITE, QUADRAT_HOEHE, autos):
    for zeile in range(len(spielfeld_map)):
        if spielfeld_map[zeile] == strasse:
            # Wenn Timer abgelaufen, neues Auto spawnen
            if timer_runterzaehlen(zeile):
                # Richtung der Strasse holen
                richtung = strasse_richtungen[zeile]

                auto = Auto(0, 0, richtung)

                # Auto an der Seite spawnen
                if richtung == 1:
                    auto_x = -auto.breite
                
                else:
                    auto_x = SPIELFELD_BREITE * QUADRAT_BREITE + auto.breite
                
                # Auto Y Position festlegen
                auto_y = zeile * QUADRAT_HOEHE + QUADRAT_HOEHE / 10 - y_verschiebung

                auto.x = auto_x
                auto.y = auto_y

                # Auto zur Liste hinzufügen
                autos.append(auto)


def kollision_erkennen(spieler, autos):
    # Spieler Rechteck holen
    spieler_rechteck = pygame.Rect(spieler.x, spieler.y, spieler.breite, spieler.hoehe)

    # Autos durchgehen und Kollision prüfen
    for auto in autos:
        auto_rechteck = pygame.Rect(auto.x, auto.y + y_verschiebung, auto.breite, auto.hoehe)

        # Kollision prüfen
        if spieler_rechteck.colliderect(auto_rechteck):
            return True
    
    return False


def auto_bewegen(autos):
    for auto in autos:
        auto.bewegen()
        

def hochgehen(QUADRAT_BREITE, QUADRAT_HOEHE, autos):
	global y_verschiebung

	y_verschiebung += QUADRAT_HOEHE

	spielfeld_map.pop(-1)
	neues_feld = random.choice(BODEN)
	spielfeld_map.insert(0, neues_feld)

	# Alle Listen und Dictionaries updaten
	for key in sorted(strasse_richtungen.keys(), reverse=True):
		strasse_richtungen[key + 1] = strasse_richtungen.pop(key)

	for key in sorted(strasse_intervalle.keys(), reverse=True):
		strasse_intervalle[key + 1] = strasse_intervalle.pop(key)

	for key in sorted(strasse_timer.keys(), reverse=True):
		strasse_timer[key + 1] = strasse_timer.pop(key)

	# Wenn neues Feld eine Strasse ist, Autos und Intervalle festlegen
	if neues_feld == strasse:
		strasse_befüllen(0, QUADRAT_BREITE, QUADRAT_HOEHE, autos)
		intervall_festlegen(0)


def reset():
    global strasse_richtungen, strasse_timer, strasse_intervalle, spielfeld_map, y_verschiebung

    strasse_richtungen = {}
    strasse_timer = {}
    strasse_intervalle = {}
    spielfeld_map = []

    y_verschiebung = 0