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
def dashboard_env(tmp_path):
    # Create an isolated SQLite database for each test.
    database_path = tmp_path / "test_dashboard.db"

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


def create_action_log(db, action_type_id, points, co2, category="Test"):
    action = ActionLog(
        action_type_id=action_type_id,
        date=datetime.date(2026, 1, 10),
        description="Dashboard test",
        category=category,
        points_awarded=points,
        co2_awarded=co2,
    )
    db.add(action)
    db.commit()


def test_dashboard_without_actions(dashboard_env):
    client, _db = dashboard_env

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert response.json() == {
        "total_points": 0,
        "current_level": "Seed",
        "total_actions": 0,
        "total_co2_impact_kg": 0.0,
    }


def test_dashboard_aggregates_statistics(dashboard_env):
    client, db = dashboard_env
    action_type = create_action_type(db)

    create_action_log(db, action_type.id, 40, 1.234)
    create_action_log(db, action_type.id, 110, 0.125)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert response.json() == {
        "total_points": 150,
        "current_level": "Sprout",
        "total_actions": 2,
        "total_co2_impact_kg": 1.36,
    }


@pytest.mark.parametrize(
    "points, expected_level",
    [
        (0, "Seed"),
        (99, "Seed"),
        (100, "Sprout"),
        (299, "Sprout"),
        (300, "Tree"),
        (699, "Tree"),
        (700, "Forest"),
        (1499, "Forest"),
        (1500, "Planet Hero"),
    ],
)
def test_dashboard_level_thresholds(dashboard_env, points, expected_level):
    client, db = dashboard_env
    action_type = create_action_type(db)

    create_action_log(db, action_type.id, points, 0.5)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert response.json()["total_points"] == points
    assert response.json()["current_level"] == expected_level