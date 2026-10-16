import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.database.database import Base
from app.models.action_type_model import ActionLog, ActionType
from app.routes.points import level_for


@pytest.fixture
def points_env(tmp_path):
    # Creamos una base de datos temporal para las pruebas.
    database_path = tmp_path / "test_points.db"

    test_engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=test_engine)

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
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


def create_action_type(db):
    action_type = ActionType(
        name="Test sustainable action",
        category="Test",
        points=10,
        co2_kg=1.0,
        active=True,
    )
    db.add(action_type)
    db.commit()
    db.refresh(action_type)
    return action_type


def create_action_log(db, action_type_id, points):
    action = ActionLog(
        action_type_id=action_type_id,
        date=datetime.date(2026, 1, 10),
        description="Points test",
        points_awarded=points,
        co2_awarded=1.0,
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return action


def test_level_for_thresholds():
    assert level_for(0) == "Seed"
    assert level_for(99) == "Seed"

    assert level_for(100) == "Sprout"
    assert level_for(299) == "Sprout"

    assert level_for(300) == "Tree"
    assert level_for(699) == "Tree"

    assert level_for(700) == "Forest"
    assert level_for(1499) == "Forest"

    assert level_for(1500) == "Planet Hero"
    assert level_for(2500) == "Planet Hero"


def test_add_points_endpoint_returns_registered_action_points(points_env):
    client, db = points_env
    action_type = create_action_type(db)
    create_action_log(db, action_type.id, 150)

    # El endpoint consulta los puntos guardados; no los suma manualmente.
    response = client.post("/user/test_user/points")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "test_user",
        "points": 150,
        "level": "Sprout",
    }


def test_get_points_endpoint(points_env):
    client, db = points_env
    action_type = create_action_type(db)
    create_action_log(db, action_type.id, 250)

    response = client.get("/user/test_user/points")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "test_user",
        "points": 250,
        "level": "Sprout",
        "next_level": "Tree",
        "points_to_next_level": 50,
    }


def test_get_points_user_not_found(points_env):
    client, _db = points_env

    response = client.get("/user/usuario_fantasma/points")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Usuario no encontrado"
    }
