import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.database.database import Base
from app.models.action_type_model import ActionLog, ActionType


client = TestClient(app)


@pytest.fixture
def catalog_env(tmp_path):
    database_path = tmp_path / "test_catalog.db"
    test_engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=test_engine)
    testing_session_local = sessionmaker(
        bind=test_engine, autoflush=False, autocommit=False
    )
    db = testing_session_local()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    try:
        yield test_client, db
    finally:
        app.dependency_overrides.pop(get_db, None)
        db.close()
        test_engine.dispose()


def test_get_catalog():
    """Prueba que el catálogo devuelva una lista con un código 200 OK"""
    response = client.get("/catalog")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_catalog_action_fields(catalog_env):
    test_client, db = catalog_env
    action_type = ActionType(
        name="Reciclar",
        category="Reciclaje",
        points=5,
        co2_kg=1.0,
        active=True,
    )
    db.add(action_type)
    db.commit()
    db.refresh(action_type)

    db.add(
        ActionLog(
            action_type_id=action_type.id,
            date=datetime.date(2026, 1, 1),
            description="Reciclaje registrado",
            category=action_type.category,
            points_awarded=action_type.points,
            co2_awarded=action_type.co2_kg,
        )
    )
    db.commit()

    response = test_client.put(
        f"/catalog/{action_type.id}",
        json={
            "name": "Reciclar vidrio",
            "category": "Residuos",
            "points": 12,
            "co2_kg": 2.5,
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Reciclar vidrio"
    assert response.json()["category"] == "Residuos"
    assert response.json()["points"] == 12
    assert response.json()["co2_kg"] == 2.5

    existing_log = db.scalar(select(ActionLog))
    assert existing_log.category == "Reciclaje"
    assert existing_log.points_awarded == 5
    assert existing_log.co2_awarded == 1.0


def test_update_catalog_action_not_found(catalog_env):
    test_client = catalog_env[0]

    response = test_client.put("/catalog/9999", json={"points": 10})

    assert response.status_code == 404


def test_register_action_future_date():
    """Prueba la regla de negocio: no se pueden registrar acciones en el futuro"""
    payload = {
        "action_type_id": 1,
        "action_date": "2050-01-01",  
        "notes": "Test de viaje en el tiempo"
    }
    response = client.post("/actions/", json=payload)
    
    
    assert response.status_code == 400
    assert response.json()["detail"] == "La fecha de la acción no puede ser en el futuro."

def test_register_action_invalid_catalog_id():
    """Prueba la regla de negocio: el ID del catálogo debe existir"""
    payload = {
        "action_type_id": 99999,  
        "action_date": "2023-01-01",
        "notes": "Test de acción inventada"
    }
    response = client.post("/actions/", json=payload)
    
    
    assert response.status_code == 404
    assert response.json()["detail"] == "El tipo de acción seleccionada no existe en el catálogo."