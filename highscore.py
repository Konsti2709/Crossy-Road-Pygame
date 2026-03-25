import json

highscores = []
max_highscores_anzahl = 10

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


def highscore_liste_speichern():
    with open("crossyroad_highscores.json", "w") as datei:
        json.dump(highscores, datei)


def highscore_liste_laden():
    global highscores
    # Highscores aus Datei laden
    try:
        highscore_liste_laden()
        
        for highscore in highscores:
            highscore["score"] = int(highscore["score"])
    except:
        highscore_liste_speichern()
