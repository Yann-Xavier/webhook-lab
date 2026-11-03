import os
import sqlite3
from contextlib import closing

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Event(BaseModel):
    id: str
    message: str


@app.post("/events")
def receive(event: Event):
    path = os.getenv("WEBHOOK_DB", "events.sqlite3")
    with closing(sqlite3.connect(path)) as connection, connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS events "
            "(id TEXT PRIMARY KEY, message TEXT NOT NULL)"
        )
        result = connection.execute(
            "INSERT INTO events VALUES (?, ?) ON CONFLICT(id) DO NOTHING",
            (event.id, event.message),
        )
        return {"accepted": result.rowcount == 1}
