from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import ActionCreate
from app.controller import action_controller

router = APIRouter(
    prefix="/actions",
    tags=["Actions Registration"]
)

@router.post("/")
def register_action(action_data: ActionCreate, db: Session = Depends(get_db)):
    # Pasamos toda la responsabilidad al controlador
    return action_controller.create_action_log(db, action_data)