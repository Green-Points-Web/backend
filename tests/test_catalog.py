from fastapi.testclient import TestClient
# Importamos la app principal desde nuestra carpeta app
from app.main import app

# Creamos un cliente de pruebas que simula ser un navegador o frontend
client = TestClient(app)

def test_get_catalog():
    """Prueba que el catálogo devuelva una lista con un código 200 OK"""
    response = client.get("/catalog")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_register_action_future_date():
    """Prueba la regla de negocio: no se pueden registrar acciones en el futuro"""
    payload = {
        "action_type_id": 1,
        "action_date": "2050-01-01",  # Fecha futura simulada
        "notes": "Test de viaje en el tiempo"
    }
    response = client.post("/actions/", json=payload)
    
    # Esperamos un error 400 Bad Request que programaste en actions.py
    assert response.status_code == 400
    assert response.json()["detail"] == "La fecha de la acción no puede ser en el futuro."

def test_register_action_invalid_catalog_id():
    """Prueba la regla de negocio: el ID del catálogo debe existir"""
    payload = {
        "action_type_id": 99999,  # ID que no existe
        "action_date": "2023-01-01",
        "notes": "Test de acción inventada"
    }
    response = client.post("/actions/", json=payload)
    
    # Esperamos un error 404 Not Found que programaste en actions.py
    assert response.status_code == 404
    assert response.json()["detail"] == "El tipo de acción seleccionada no existe en el catálogo."