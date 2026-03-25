# Imports
import pygame
import random
import json

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

# Spielergrösse
SPIELER_BREITE = 40
SPIELER_HOEHE = 40

# Autogrösse
AUTO_BREITE = 40
AUTO_HOEHE = 40 

# Uhr für die FPS
clock = pygame.time.Clock()

# Highscoreliste
highscores = []
max_highscores_anzahl = 10
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
    for auto_pos in auto_positionen:
        auto_x = auto_pos[0]
        auto_y = auto_pos[1]

        # Auto erstellen
        quadrat = pygame.Rect(auto_x, auto_y + y_verschiebung, AUTO_BREITE, AUTO_HOEHE)

        # Auto zeichnen 
        pygame.draw.rect(FENSTER, "blue", quadrat)  

    # Spieler erstellen
    quadrat = pygame.Rect(spieler_x, spieler_y, SPIELER_BREITE, SPIELER_HOEHE)

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

        # Auto zur Liste hinzufügen
        auto_positionen.append((auto_x, auto_y))

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


def auto_spawnen():
    for zeile in range(len(spielfeld_map)):
        if spielfeld_map[zeile] == strasse:
            # Wenn Timer abgelaufen, neues Auto spawnen
            if timer_runterzaehlen(zeile):
                # Richtung der Strasse holen
                richtung = strasse_richtungen[zeile]
                # Auto an der Seite spawnen
                if richtung == 1:
                    auto_x = -AUTO_BREITE
                
                else:
                    auto_x = BREITE + AUTO_BREITE
                
                # Auto Y Position festlegen
                auto_y = zeile * QUADRAT_HOEHE + QUADRAT_HOEHE / 10 - y_verschiebung

                # Auto zur Liste hinzufügen
                auto_positionen.append((auto_x, auto_y))


def kollision_erkennen():
    # Spieler Rechteck holen
    spieler_rechteck = pygame.Rect(spieler_x, spieler_y, SPIELER_BREITE, SPIELER_HOEHE)

    # Autos durchgehen und Kollision prüfen
    for auto in range(len(auto_positionen)):
        auto_x, auto_y = auto_positionen[auto]
        auto_rechteck = pygame.Rect(auto_x, auto_y + y_verschiebung, AUTO_BREITE, AUTO_HOEHE)

        # Kollision prüfen
        kollision = spieler_rechteck.colliderect(auto_rechteck)
        if kollision:
            return True
    
    return False


def auto_bewegen():
    for auto in range(len(auto_positionen)):
        # Zeile und Richtung holen
        zeile = (auto_positionen[auto][1] + y_verschiebung) // QUADRAT_HOEHE
        richtung = strasse_richtungen[zeile]

        # Auto Position updaten
        auto_x, auto_y = auto_positionen[auto]
        auto_x += richtung

        # geänderte Position speichern
        auto_positionen[auto] = (auto_x, auto_y)


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


def highscore_hinzufügen(name, neuer_score):
    global highscores

    # Neuen Score zu Zahl umwandeln
    neuer_score = int(neuer_score)

    # Name und Score zur Highscoreliste hinzufügen
    highscores.append({"name": name, "score": neuer_score})

    # Highscores sortieren
    for i in range(len(highscores)):
        for j in range(i + 1, len(highscores)):
            if highscores[j]["score"] > highscores[i]["score"]:
                highscores[i], highscores[j] = highscores[j], highscores[i]
    
    # Highscoreliste auf max Anzahl kürzen
    highscores = highscores[:max_highscores_anzahl]

    # Speichern
    highscore_liste_speichern()
    

def highscores_anzeigen():
    y_position = 200

    # Tabelle zeichnen
    for highscore in highscores:
        platzierung = highscores.index(highscore) + 1
        name = highscore["name"]
        score = highscore["score"]
        text = str(platzierung) + ". " + name + " - " + str(score)
        text_anzeigen(text, 60, (BREITE // 2 - 150, y_position))
        y_position += 70


def highscore_liste_speichern():
    with open("crossyroad_highscores.json", "w") as datei:
        json.dump(highscores, datei)


def highscore_liste_laden():
    global highscores
    with open("crossyroad_highscores.json", "r") as datei:
        highscores = json.load(datei)


def reset_game():
    # Variablen global machen
    global spieler_x, spieler_y, auto_positionen, strasse_richtungen
    global strasse_timer, strasse_intervalle, spielfeld_map
    global y_verschiebung, score, frame_count, running, game_over, top_10_gecheckt

    # Spielerposition zurücksetzen
    spieler_x = 10 * QUADRAT_BREITE + QUADRAT_BREITE / 10
    spieler_y = 10 * QUADRAT_HOEHE + QUADRAT_HOEHE / 10

    # Alle Listen und Dictionaries leeren
    auto_positionen = []
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


# Highscores aus Datei laden
try:
    highscore_liste_laden()
    
    for highscore in highscores:
        highscore["score"] = int(highscore["score"])
except:
    highscore_liste_speichern()

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
                    highscore_hinzufügen(name, score)
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
                    if spieler_y <= 10 * QUADRAT_HOEHE:

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
                        spieler_y -= QUADRAT_HOEHE

                # Unten
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:           
                    spieler_y += QUADRAT_HOEHE
                
                # Links
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:           
                    spieler_x -= QUADRAT_BREITE
                
                # Rechts
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:           
                    spieler_x += QUADRAT_BREITE

    if game_over and not top_10_gecheckt:
        # Prüfen, ob Score in Top 10 ist
        if len(highscores) < max_highscores_anzahl or score > highscores[-1]["score"]:
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


