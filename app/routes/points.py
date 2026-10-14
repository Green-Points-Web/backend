from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
router = APIRouter()
app.include_router(router)

user_points: dict[str, int] = {}

class PointsRequest(BaseModel):
    user_id: str = Field(..., description="El ID del usuario")
    points: int = Field(..., description="El número de puntos a agregar o restar")

def level_for(points: int) -> str:
    if points < 100:
        return "Semilla"
    if points < 300:
        return "Brote"
    if points < 700:
        return "Arbol"
    if points < 1500:
        return "Bosque"
    return "Heroe del planeta" 

 

