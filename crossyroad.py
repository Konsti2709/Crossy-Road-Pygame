# Imports
import pygame
import random
import highscore
from spieler import Spieler
from autos import Auto

# Initialisierung der Pygame-Module
pygame.init()

# Spielfeldgrösse
SPIELFELD_BREITE = 20
SPIELFELD_HOEHE = 20

# Vorgenerierters Spielfeld
VORGENERIERT_BREITE = 20
VORGENERIERT_HOEHE = 20

# Feldergrösse
QUADRAT_BREITE = 50
QUADRAT_HOEHE = 50

# Fenster erstellen
BREITE = SPIELFELD_BREITE * QUADRAT_BREITE
HOEHE = SPIELFELD_HOEHE * QUADRAT_HOEHE
FENSTER = pygame.display.set_mode((BREITE, HOEHE))

# Überschrift erstellen
pygame.display.set_caption("Crossy Road")

# Farben verschiedener Bodenarten
gras = "green"
strasse = "gray"
wasser = "lightblue"

# Bodenarten Liste
BODEN = [gras, strasse, wasser]

# Uhr für die FPS
clock = pygame.time.Clock()

# Highscoreliste
highscore_anzeige_modus = False


# Spielfeld generieren
def spielfeld():      
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
        quadrat = pygame.Rect(0, zeile * QUADRAT_HOEHE, BREITE, QUADRAT_HOEHE)

        # fenster, farbe, objekt
        pygame.draw.rect(FENSTER, farbe, quadrat)
    
    # Autopositionen durchgehen
    for auto in autos:
        # Auto erstellen
        quadrat = pygame.Rect(auto.x, auto.y + y_verschiebung, Auto.breite, Auto.hoehe)

        # Auto zeichnen 
        pygame.draw.rect(FENSTER, "blue", quadrat)  

    # Spieler erstellen
    quadrat = pygame.Rect(spieler.x, spieler.y, spieler.breite, spieler.hoehe)

    # Spieler zeichnen
    pygame.draw.rect(FENSTER, "red", quadrat)


def strasse_befüllen(zeile):
    # Random Anzahl Autos und Richtung
    anzahl_autos = random.randint(4, 6)
    richtung = random.choice([-1, 1])

    # Autos setzen
    for auto in range(anzahl_autos):

        # Random X Position
        auto_x = random.randint(0, SPIELFELD_BREITE) * QUADRAT_BREITE + QUADRAT_BREITE / 10
        
        # Random Y Position
        auto_y = zeile * QUADRAT_HOEHE + QUADRAT_HOEHE / 10 - y_verschiebung

        # Richtung der Strasse speichern für spätere Autos
        strasse_richtungen[zeile] = richtung
        
        # Auto zur Liste hinzufügen
        autos.append(Auto(auto_x, auto_y, richtung))


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


def auto_spawnen():
    for zeile in range(len(spielfeld_map)):
        if spielfeld_map[zeile] == strasse:
            # Wenn Timer abgelaufen, neues Auto spawnen
            if timer_runterzaehlen(zeile):
                # Richtung der Strasse holen
                richtung = strasse_richtungen[zeile]

                # Auto an der Seite spawnen
                if richtung == 1:
                    auto_x = -Auto.breite
                
                else:
                    auto_x = BREITE + Auto.breite
                
                # Auto Y Position festlegen
                auto_y = zeile * QUADRAT_HOEHE + QUADRAT_HOEHE / 10 - y_verschiebung

                # Auto zur Liste hinzufügen
                autos.append(Auto(auto_x, auto_y, richtung))


def kollision_erkennen():
    # Spieler Rechteck holen
    spieler_rechteck = pygame.Rect(spieler.x, spieler.y, spieler.breite, spieler.hoehe)

    # Autos durchgehen und Kollision prüfen
    for auto in autos:
        auto_rechteck = pygame.Rect(auto.x, auto.y + y_verschiebung, auto.breite, auto.hoehe)

        # Kollision prüfen
        if spieler_rechteck.colliderect(auto_rechteck):
            return True
    
    return False


def auto_bewegen():
    for auto in autos:
        auto.bewegen()


def score_anzeigen(groesse, position):
    # Schrift erstellen
    font = pygame.font.Font(None, groesse)
    # Text erstellen
    text = font.render("Score: " + str(score), True, "white")
    # Text ins Fenster zeichnen
    FENSTER.blit(text, position)


def text_anzeigen(text_string, groesse, position):
    # Schrift erstellen
    font = pygame.font.Font(None, groesse)
    # Text erstellen
    text = font.render(text_string, True, "white")
    # Text ins Fenster zeichnen
    FENSTER.blit(text, position)


def reset_game():
    # Variablen global machen
    global spieler, autos, strasse_richtungen
    global strasse_timer, strasse_intervalle, spielfeld_map
    global y_verschiebung, score, frame_count, running, game_over, top_10_gecheckt

    # Spielerposition zurücksetzen
    start_x = 10 * QUADRAT_BREITE + QUADRAT_BREITE / 10
    start_y = 10 * QUADRAT_HOEHE + QUADRAT_HOEHE / 10

    spieler = Spieler(start_x, start_y)

    # Alle Listen und Dictionaries leeren
    autos = []
    strasse_richtungen = {}
    strasse_timer = {}
    strasse_intervalle = {}
    spielfeld_map = []

    # Verschiebung und Score zurücksetzen
    y_verschiebung = 0
    score = 0
    frame_count = 0
    running = True
    game_over = False
    top_10_gecheckt = False

    # Spielfeld neu generieren
    for zeile in range(SPIELFELD_HOEHE):
        
        # Farbe und Feld festlegen
        feld = random.choice(BODEN)
        if feld == gras:
            farbe = gras
        elif feld == strasse:
            farbe = strasse
        elif feld == wasser:
            farbe = wasser

        # links oben x, links oben y, breite, höhe
        quadrat = pygame.Rect(0, zeile * QUADRAT_HOEHE, BREITE, QUADRAT_HOEHE)
        # fenster, farbe, objekt

        pygame.draw.rect(FENSTER, farbe, quadrat)

        # Spielfeld in Liste speichern
        spielfeld_map.append(feld)

    # Für jede Strasse Autos und Intervalle festlegen
    for zeile in range(len(spielfeld_map)):
        if spielfeld_map[zeile] == strasse:
            strasse_befüllen(zeile)
            intervall_festlegen(zeile)


def highscores_anzeigen():
    y_position = 200

    # Tabelle zeichnen
    for i, h in enumerate(highscore.top_10_laden()):
        platzierung = i + 1
        name, score = h
        text = str(platzierung) + ". " + name + " - " + str(score)
        text_anzeigen(text, 60, (BREITE // 2 - 150, y_position))
        y_position += 70


# Name
name = ""
name_eingabe = False


# Ganz am Anfang das Spiel resetten
reset_game()


# Hauptschleife
while running:

    # Nach Events schauen
    for event in pygame.event.get():

        # Spiel beenden
        if event.type == pygame.QUIT:
            pygame.quit()

        

        # Spieler bewegen
        if event.type == pygame.KEYDOWN:
            
            # Spiel resetten
            if game_over and event.key == pygame.K_RETURN and not name_eingabe:
                game_over = False
                reset_game()
            
            # Name eingeben
            if game_over and name_eingabe:

                if event.key == pygame.K_RETURN:
                    highscore.highscore_hinzufügen(name, score)
                    name_eingabe = False
                    name = ""

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif event.unicode.isprintable():
                    name += event.unicode
            
            # Highscoreanzeige Modus aktivieren
            if game_over and not name_eingabe and event.key == pygame.K_h:
                highscore_anzeige_modus = True
            
            # Highscoreanzeige Modus deaktivieren
            if highscore_anzeige_modus and event.key == pygame.K_ESCAPE:
                highscore_anzeige_modus = False

            # Movement
            if not game_over:
                # Oben
                if event.key == pygame.K_w or event.key == pygame.K_UP:

                    # Überprüfen, ob Spielfeld verschoben werden muss
                    if spieler.y <= 10 * QUADRAT_HOEHE:

                        # Spielfeld verschieben
                        y_verschiebung += QUADRAT_HOEHE

                        # Score erhöhen
                        score += 1

                        # Unterste Zeile entfernen und neue Zeile oben hinzufügen
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
                            strasse_befüllen(0)
                            intervall_festlegen(0)

                    # Spieler normal bewegen
                    else:
                        spieler.bewegen(0, -QUADRAT_HOEHE)

                # Unten
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:           
                    spieler.bewegen(0, QUADRAT_HOEHE)
                
                # Links
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:           
                    spieler.bewegen(-QUADRAT_BREITE, 0)
                
                # Rechts
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:           
                    spieler.bewegen(QUADRAT_BREITE, 0)

    if game_over and not top_10_gecheckt:
        # Prüfen, ob Score in Top 10 ist
        if highscore.ist_top_10(score):
            name_eingabe = True

        else:
            name_eingabe = False
    
        top_10_gecheckt = True

    if not game_over:
        # Falls Kollision, Spiel beenden
        if kollision_erkennen():
            game_over = True
        
        # Autos bewegen
        auto_bewegen()

        # Autos spawnen
        auto_spawnen()

        # Spielfeld neu zeichnen
        spielfeld()

        # Score anzeigen
        score_anzeigen(50, (10, 10))

    # Bildschirm aktualisieren
    pygame.display.update()

    # Framecount erhöhen
    frame_count += 1

    # FPS einstellen
    clock.tick(60)

    # Game Over Bildschirm
    if game_over:
        FENSTER.fill("black")

        if name_eingabe:
            text_anzeigen("Name: " + name, 100, (200, 400))

        elif highscore_anzeige_modus:
            highscores_anzeigen()  
  
        else:
            text_anzeigen("Enter drücken, um\n neu zu starten", 100, (BREITE / 2 - 275, HOEHE / 2 + 100))
            score_anzeigen(100, (BREITE // 2 - 120, HOEHE // 2 - 150))     


