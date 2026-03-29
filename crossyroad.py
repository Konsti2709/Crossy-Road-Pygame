# Imports
import pygame
import spielfeld
import highscore
from spieler import Spieler

# Initialisierung der Pygame-Module
pygame.init()

SPIELFELD_BREITE = 20
SPIELFELD_HOEHE = 20

# Feldergrösse
QUADRAT_BREITE = 50
QUADRAT_HOEHE = 50

# Fenster erstellen
BREITE = SPIELFELD_BREITE * QUADRAT_BREITE
HOEHE = SPIELFELD_HOEHE * QUADRAT_HOEHE
FENSTER = pygame.display.set_mode((BREITE, HOEHE))

# Überschrift erstellen
pygame.display.set_caption("Crossy Road")

# Uhr für die FPS
clock = pygame.time.Clock()

# Highscoreliste
highscore_anzeige_modus = False


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
    global spieler, autos
    global score, frame_count, running, game_over, top_10_gecheckt

    # Spielerposition zurücksetzen
    start_x = 10 * QUADRAT_BREITE + QUADRAT_BREITE / 10
    start_y = 10 * QUADRAT_HOEHE + QUADRAT_HOEHE / 10

    spieler = Spieler(start_x, start_y)

    # Alle Listen und Dictionaries leeren
    autos = []

    # Verschiebung und Score zurücksetzen
    score = 0
    frame_count = 0
    running = True
    game_over = False
    top_10_gecheckt = False
    
    spielfeld.neu_generieren(FENSTER, QUADRAT_HOEHE, QUADRAT_BREITE, autos)


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
                        score += 1
                        spielfeld.hochgehen(QUADRAT_BREITE, QUADRAT_HOEHE, autos)

                    # Spieler normal bewegen
                    else:
                        spieler.bewegen(0, -QUADRAT_HOEHE, BREITE, HOEHE)

                # Unten
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:           
                    spieler.bewegen(0, QUADRAT_HOEHE, BREITE, HOEHE)
                
                # Links
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:           
                    spieler.bewegen(-QUADRAT_BREITE, 0, BREITE, HOEHE)
                
                # Rechts
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:           
                    spieler.bewegen(QUADRAT_BREITE, 0, BREITE, HOEHE)

    if game_over and not top_10_gecheckt:
        # Prüfen, ob Score in Top 10 ist
        if highscore.ist_top_10(score):
            name_eingabe = True

        else:
            name_eingabe = False
    
        top_10_gecheckt = True

    if not game_over:
        # Falls Kollision, Spiel beenden
        if spielfeld.kollision_erkennen(spieler, autos):
            game_over = True
        
        # Autos bewegen
        spielfeld.auto_bewegen(autos)

        # Autos spawnen
        spielfeld.auto_spawnen(QUADRAT_BREITE, QUADRAT_HOEHE, autos)

        # Spielfeld neu zeichnen
        spielfeld.generieren(FENSTER, QUADRAT_HOEHE, QUADRAT_BREITE, autos, spieler)

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
