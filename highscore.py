import sqlite3

conn = sqlite3.connect("crossyroad_highscores.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS Highscores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    score INTEGER
)           
""")

conn.commit()


def highscore_hinzufügen(name, score):
    cursor.execute(
        "INSERT INTO Highscores (name, score) VALUES (?, ?)",
        (name, int(score))
    )
    conn.commit()


def top_10_laden():
    cursor.execute(
        "SELECT name, score FROM Highscores ORDER BY score DESC LIMIT 10"
    )

    return cursor.fetchall()


def ist_top_10(score):
    cursor.execute(
        "SELECT name, score FROM Highscores ORDER BY score DESC LIMIT 10"
    )

    top_10_scores = cursor.fetchall()


    if len(top_10_scores) < 10:
        return True
    
    return score > top_10_scores[-1][1]
