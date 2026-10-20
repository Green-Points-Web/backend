import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.database.database import Base
from app.models.action_type_model import ActionLog, ActionType


@pytest.fixture
def history_env(tmp_path):
    database_path = tmp_path / "test_history.db"

    test_engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=test_engine)

    TestingSessionLocal = sessionmaker(
        bind=test_engine, autoflush=False, autocommit=False
    )
    db = TestingSessionLocal()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    try:
        yield client, db
    finally:
        app.dependency_overrides.pop(get_db, None)
        db.close()
        test_engine.dispose()


def _action_type(db, **overrides):
    values = {
        "name": "Reciclar",
        "category": "Reciclaje",
        "points": 5,
        "co2_kg": 1.0,
        "active": True,
    }
    values.update(overrides)
    action_type = ActionType(**values)
    db.add(action_type)
    db.commit()
    db.refresh(action_type)
    return action_type


def _action_log(db, action_type_id, action_date, description, points, co2, category):
    log = ActionLog(
        action_type_id=action_type_id,
        date=action_date,
        description=description,
        category=category,
        points_awarded=points,
        co2_awarded=co2,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def test_history_empty(history_env):
    client, _db = history_env

    response = client.get("/history")

    assert response.status_code == 200
    assert response.json() == []


def test_history_response_shape(history_env):
    client, db = history_env
    at = _action_type(db, name="Ir en bici", category="Movilidad", points=15, co2_kg=2.0)
    _action_log(db, at.id, datetime.date(2026, 2, 10), "Bici", 15, 2.0, at.category)

    body = client.get("/history").json()

    assert len(body) == 1
    assert body[0]["action_type_id"] == at.id
    assert body[0]["action_date"] == "2026-02-10"
    assert body[0]["description"] == "Bici"
    assert body[0]["points_earned"] == 15
    assert body[0]["co2_saved"] == 2.0
    assert body[0]["category"] == "Movilidad"


def test_history_newest_first(history_env):
    client, db = history_env
    at = _action_type(db)
    _action_log(db, at.id, datetime.date(2026, 1, 1), "viejo", 5, 1.0, at.category)
    _action_log(db, at.id, datetime.date(2026, 3, 1), "nuevo", 5, 1.0, at.category)


    body = client.get("/history").json()

    assert [r["description"] for r in body] == ["nuevo", "viejo"]


def test_history_keeps_points_snapshot(history_env):
    client, db = history_env
    at = _action_type(db, points=5)
    _action_log(db, at.id, datetime.date(2026, 1, 1), "Reciclé", 5, 1.0, at.category)

    at.points = 999
    db.commit()

    body = client.get("/history").json()

    assert body[0]["points_earned"] == 5

def test_history_keeps_category_snapshot(history_env):
    client, db = history_env
    at = _action_type(db, category="Reciclaje")
    _action_log(db, at.id, datetime.date(2026, 1, 1), "Reciclé", 5, 1.0, category="Reciclaje")

    at.category = "Residuos"
    db.commit()

    body = client.get("/history").json()

    assert body[0]["category"] == "Reciclaje" 

def test_history_filter_by_date_range(history_env):
    client, db = history_env
    at = _action_type(db)
    _action_log(db, at.id, datetime.date(2026, 1, 1), "enero", 5, 1.0, at.category)
    _action_log(db, at.id, datetime.date(2026, 6, 1), "junio", 5, 1.0, at.category)

    body = client.get("/history", params={"start_date": "2026-05-01"}).json()

    assert [r["description"] for r in body] == ["junio"]


def test_update_history_action(history_env):
    client, db = history_env
    at = _action_type(db)
    action = _action_log(
        db, at.id, datetime.date(2026, 1, 1), "Original", 5, 1.0, at.category
    )

    response = client.put(
        f"/history/{action.id}",
        json={"date": "2026-02-10", "description": "Actualizada"},
    )

    assert response.status_code == 200
    assert response.json()["action_date"] == "2026-02-10"
    assert response.json()["description"] == "Actualizada"


def test_update_history_action_rejects_future_date(history_env):
    client, db = history_env
    at = _action_type(db)
    action = _action_log(
        db, at.id, datetime.date(2026, 1, 1), "Original", 5, 1.0, at.category
    )

    response = client.put(
        f"/history/{action.id}",
        json={"date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat()},
    )

    assert response.status_code == 400


def test_delete_history_action(history_env):
    client, db = history_env
    at = _action_type(db)
    action = _action_log(
        db, at.id, datetime.date(2026, 1, 1), "Eliminar", 5, 1.0, at.category
    )

    response = client.delete(f"/history/{action.id}")

    assert response.status_code == 204
    assert db.get(ActionLog, action.id) is None