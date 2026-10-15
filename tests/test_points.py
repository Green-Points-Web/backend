from fastapi.testclient import TestClient
from backend.routes.points import app, level_for, user_points

client = TestClient(app)

def setup_function():
    
    user_points.clear()