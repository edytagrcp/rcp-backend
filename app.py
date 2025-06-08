from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogEntry(BaseModel):
    pracownik: str
    data: str
    start: str
    koniec: str
    czas_pracy: Optional[str] = None
    bezczynnosc: Optional[str] = None
    bezczynnosc_5min: Optional[str] = None
    start_przerwy: Optional[str] = None
    koniec_przerwy: Optional[str] = None
    czas_przerwy: Optional[str] = None
    lokalizacja: Optional[str] = None

log_storage: List[LogEntry] = []

@app.post("/log")
def add_log(entry: LogEntry):
    log_storage.append(entry)
    return {"status": "ok"}

@app.get("/logs")
def get_logs():
    return {"dane": [entry.dict() for entry in log_storage]}
