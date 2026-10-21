from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.controller import points_controller

router = APIRouter(tags=["Points"])

@router.post("/user/{user_id}/points")
def add_points(user_id: str, db: Session = Depends(get_db)):
    return points_controller.add_user_points(db=db, user_id=user_id)

@router.get("/user/{user_id}/points")
def get_points(user_id: str, db: Session = Depends(get_db)):
    return points_controller.get_user_points(db=db, user_id=user_id)