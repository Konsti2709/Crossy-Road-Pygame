import pygame
import random
from strassen import Strasse

SPIELFELD_BREITE = 20
SPIELFELD_HOEHE = 20

farbe_gras = "green"
farbe_strasse = "gray"
farbe_wasser = "lightblue"

BODEN = [farbe_gras, farbe_strasse, farbe_wasser]

strassen = []
spielfeld_map = []

y_verschiebung = 0

# Spielfeld generieren
def generieren(FENSTER, QUADRAT_HOEHE, QUADRAT_BREITE, spieler):      
    FENSTER.fill("black")

    # Farbe festlegen und zeichnen
    for zeile in range(SPIELFELD_HOEHE):
        feld = spielfeld_map[zeile]

        if isinstance(feld, Strasse):
            farbe = farbe_strasse

        elif feld == farbe_gras:
            farbe = farbe_gras

        elif feld == farbe_wasser:
            farbe = farbe_wasser

        # links oben x, links oben y, breite, höhe
        quadrat = pygame.Rect(0, zeile * QUADRAT_HOEHE, SPIELFELD_BREITE * QUADRAT_BREITE, QUADRAT_HOEHE)

        # fenster, farbe, objekt
        pygame.draw.rect(FENSTER, farbe, quadrat)
    
    # Autopositionen durchgehen
    for strasse in strassen:
        for auto in strasse.autos:

            # Auto erstellen
            quadrat = pygame.Rect(auto.x, auto.y + y_verschiebung, auto.breite, auto.hoehe)

            # Auto zeichnen 
            pygame.draw.rect(FENSTER, "blue", quadrat)  

    # Spieler erstellen
    quadrat = pygame.Rect(spieler.x, spieler.y, spieler.breite, spieler.hoehe)

    # Spieler zeichnen
    pygame.draw.rect(FENSTER, "red", quadrat)
    

def neu_generieren(FENSTER, QUADRAT_HOEHE, QUADRAT_BREITE):
    strassen.clear()
    spielfeld_map.clear()

    for zeile in range(SPIELFELD_HOEHE):
        
        # Farbe und Feld festlegen
        if zeile >= 10:
            feld = farbe_gras
        else:
            feld = random.choice(BODEN)
        
        quadrat = pygame.Rect(0, zeile * QUADRAT_HOEHE, SPIELFELD_BREITE * QUADRAT_BREITE, QUADRAT_HOEHE)

        if feld == farbe_strasse:
            pygame.draw.rect(FENSTER, farbe_strasse, quadrat)
            neue_strasse = Strasse(zeile, QUADRAT_BREITE, QUADRAT_HOEHE)
            strassen.append(neue_strasse)
            spielfeld_map.append(neue_strasse)
        elif feld == farbe_gras:
            pygame.draw.rect(FENSTER, farbe_gras, quadrat)
            spielfeld_map.append(feld)
        elif feld == farbe_wasser:
            pygame.draw.rect(FENSTER, farbe_wasser, quadrat)
            spielfeld_map.append(feld)       

    # Für jede Strasse Autos und Intervalle festlegen
    for strasse in strassen:
        strasse.befüllen(SPIELFELD_BREITE)


def kollision_erkennen(spieler):
    # Spieler Rechteck holen
    spieler_rechteck = pygame.Rect(spieler.x, spieler.y, spieler.breite, spieler.hoehe)

    # Autos durchgehen und Kollision prüfen
    for strasse in strassen:
        for auto in strasse.autos:
            auto_rechteck = pygame.Rect(auto.x, auto.y + y_verschiebung, auto.breite, auto.hoehe)

            # Kollision prüfen
            if spieler_rechteck.colliderect(auto_rechteck):
                return True
    
    return False
        

def hochgehen(QUADRAT_BREITE, QUADRAT_HOEHE):
    global y_verschiebung

    y_verschiebung += QUADRAT_HOEHE


    letztes_feld = spielfeld_map.pop(-1)

    if isinstance(letztes_feld, Strasse):
        strassen.pop(-1)

    neues_feld = random.choice(BODEN)
    
    # Wenn neues Feld eine Strasse ist, Autos und Intervalle festlegen
    if neues_feld == farbe_strasse:
        neue_zeile = -(y_verschiebung // QUADRAT_HOEHE)
        neue_strasse = Strasse(neue_zeile, QUADRAT_BREITE, QUADRAT_HOEHE)
        strassen.insert(0, neue_strasse)
        spielfeld_map.insert(0, neue_strasse)
        neue_strasse.befüllen(SPIELFELD_BREITE)
    else:
        spielfeld_map.insert(0, neues_feld)


def reset():
    global strasse_richtungen, strasse_timer, strasse_intervalle, spielfeld_map, y_verschiebung

    strasse_richtungen = {}
    strasse_timer = {}
    strasse_intervalle = {}
    spielfeld_map = []

    y_verschiebung = 0


def loop():
    for strasse in strassen:
        # Autos bewegen
        strasse.auto_bewegen()

        # Autos spawnens
        strasse.auto_spawnen(SPIELFELD_BREITE)