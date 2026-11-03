import sqlite3
from contextlib import closing

from fastapi.testclient import TestClient

from app import app


def test_retry_after_lost_response(tmp_path, monkeypatch):
    path = tmp_path / "events.sqlite3"
    monkeypatch.setenv("WEBHOOK_DB", str(path))
    event = {"id": "demo-1", "message": "Pedido recebido"}
    with TestClient(app) as sender:
        # O emissor descarta a resposta da primeira entrega.
        sender.post("/events", json=event)
    with TestClient(app) as sender:
        response = sender.post("/events", json=event)
        assert response.status_code == 200
        assert response.json() == {"accepted": False}
    with closing(sqlite3.connect(path)) as connection:
        assert connection.execute("SELECT * FROM events").fetchall() == [
            ("demo-1", "Pedido recebido")
        ]
