import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import db  # noqa: E402
from app import app  # noqa: E402


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_home():
    res = client().get("/")
    assert res.status_code == 200
    assert "message" in res.get_json()


def test_health():
    res = client().get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_greet_default():
    assert client().get("/greet").get_json()["greeting"] == "Hello, world!"


def test_greet_name():
    assert client().get("/greet?name=Asha").get_json()["greeting"] == "Hello, Asha!"


def test_visits(monkeypatch):
    # The tests don't need a real database: we replace the database
    # function with a fake one that always returns 7.
    monkeypatch.setattr(db, "increment_visits", lambda: 7)
    res = client().get("/visits")
    assert res.status_code == 200
    assert res.get_json() == {"visits": 7}


def test_visits_database_down(monkeypatch):
    def broken():
        raise RuntimeError("no database")

    monkeypatch.setattr(db, "increment_visits", broken)
    res = client().get("/visits")
    assert res.status_code == 503
    assert res.get_json()["error"] == "database unavailable"
