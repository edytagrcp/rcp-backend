from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "logs.db"

# Tworzenie bazy i tabeli, jeśli nie istnieją
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pracownik TEXT,
                data TEXT,
                start TEXT,
                koniec TEXT,
                czas_pracy TEXT,
                bezczynosc TEXT,
                bezczynosc5min TEXT,
                start_przerwy TEXT,
                koniec_przerwy TEXT,
                czas_przerwy TEXT,
                lokalizacja TEXT
            )
        ''')
        conn.commit()

@app.route("/log", methods=["POST"])
def log_entry():
    data = request.json
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO logs (pracownik, data, start, koniec, czas_pracy,
                              bezczynosc, bezczynosc5min, start_przerwy,
                              koniec_przerwy, czas_przerwy, lokalizacja)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get("pracownik", ""),
            data.get("data", ""),
            data.get("start", ""),
            data.get("koniec", ""),
            data.get("czas_pracy", ""),
            data.get("bezczynosc", ""),
            data.get("bezczynosc5min", ""),
            data.get("start_przerwy", ""),
            data.get("koniec_przerwy", ""),
            data.get("czas_przerwy", ""),
            data.get("lokalizacja", "")
        ))
        conn.commit()
    return {"status": "ok"}, 200

@app.route("/logs", methods=["GET"])
def get_logs():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM logs")
        rows = c.fetchall()
        col_names = [desc[0] for desc in c.description]
        log_dicts = [dict(zip(col_names[1:], row[1:])) for row in rows]  # bez 'id'
    return jsonify({"dane": log_dicts})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=10000)
