from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.controller import dashboard_controller

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("")
def get_dashboard(db: Session = Depends(get_db)):
    return dashboard_controller.get_dashboard_summary(db)