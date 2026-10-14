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

@app.post("/user/{user_id}/points")
async def add_points(user_id: str, request: PointsRequest):
    if user_id not in user_points:
        user_points[user_id] = 0
    user_points[user_id] += request.points
    return {"user_id": user_id, "points": user_points[user_id], "level": level_for(user_points[user_id])}

@app.get("/user/{user_id}/points")
async def get_points(user_id: str):
    if user_id not in user_points:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    total = user_points[user_id]
    thresholds = {
      "Semilla": 100,
      "Brote": 300,
      "Arbol": 700,
      "Bosque": 1500,
      "Heroe del planeta": float("inf")
    }

    current_level = level_for(total)
    next_threshold = thresholds.get(current_level, float("inf"))

    return {
        "user_id": user_id,
        "points": total,
        "level": current_level,
        "next_level": (
            next (
                (name for name, threshold in thresholds.items() 
                 if threshold == next_threshold),
                 None,
            )
            if next_threshold != float("inf") 
            else None
        ),
        "points_to_next_level": (
            next_threshold - total 
            if next_threshold != float("inf") 
            else None
        ),
    }
