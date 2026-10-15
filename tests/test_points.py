from fastapi.testclient import TestClient
from backend.routes.points import app, level_for, user_points

client = TestClient(app)

def setup_function():   
    user_points.clear()

def test_level_for_thresholds():
    # Semilla (< 100)
    assert level_for(0) == "Semilla"
    assert level_for(50) == "Semilla"
    assert level_for(99) == "Semilla"
    
    # Brote (100 a 299)
    assert level_for(100) == "Brote"
    assert level_for(200) == "Brote"
    assert level_for(299) == "Brote"
    
    # Arbol (300 a 699)
    assert level_for(300) == "Arbol"
    assert level_for(500) == "Arbol"
    assert level_for(699) == "Arbol"
    
    # Bosque (700 a 1499)
    assert level_for(700) == "Bosque"
    assert level_for(1000) == "Bosque"
    assert level_for(1499) == "Bosque"
    
    # Heroe del planeta (>= 1500)
    assert level_for(1500) == "Heroe del planeta"
    assert level_for(2500) == "Heroe del planeta"

def test_add_points_endpoint():
    response = client.post(
        "/user/test_user/points", 
        json={"user_id": "test_user", "points": 150}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["points"] == 150
    assert data["level"] == "Brote"

def test_get_points_endpoint():
    client.post(
        "/user/test_user/points", 
        json={"user_id": "test_user", "points": 250}
    )
    
    response = client.get("/user/test_user/points")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["points"] == 250
    assert data["level"] == "Brote"
    assert data["next_level"] == "Arbol"
    assert data["points_to_next_level"] == 50 

