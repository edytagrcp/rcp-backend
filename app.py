from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# MODEL DANYCH
class LogEntry(BaseModel):
    pracownik: str
    start: str
    koniec: str
    bezczynność: str
    lokalizacja: str

# TWORZENIE BAZY DANYCH, jeśli nie istnieje
def init_db():
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            pracownik TEXT,
            start TEXT,
            koniec TEXT,
            bezczynność TEXT,
            lokalizacja TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ENDPOINT: Dodanie logu
@app.post("/log")
def add_log(entry: LogEntry):
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)", 
              (entry.pracownik, entry.start, entry.koniec, entry.bezczynność, entry.lokalizacja))
    conn.commit()
    conn.close()
    return {"status": "OK"}

# ENDPOINT: Pobierz wszystkie logi
@app.get("/logs")
def get_logs():
    conn = sqlite3.connect("logs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    rows = c.fetchall()
    conn.close()
    return {"dane": rows}
