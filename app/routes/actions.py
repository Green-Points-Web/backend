from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.action_type_model import ActionType, ActionLog

router = APIRouter(
    prefix="/actions",
    tags=["Actions Registration"]
)


@router.post("/")
def register_action(action_data: dict, db: Session = Depends(get_db)):
    
    action_date_str = action_data.get("action_date")
    if action_date_str > str(date.today()):
        raise HTTPException(status_code=400, detail="La fecha de la acción no puede ser en el futuro.")

    action_type_id = action_data.get("action_type_id")
    action_type = db.query(ActionType).filter(ActionType.id == action_type_id).first()
    
    if not action_type:
        raise HTTPException(status_code=404, detail="El tipo de acción seleccionada no existe en el catálogo.")

    points_earned = action_type.points
    co2_saved = action_type.co2_kg  

    new_action = ActionLog(
        action_type_id=action_type.id,
        date=action_date_str,                    
        description=action_data.get("notes", ""), 
        points_awarded=points_earned,              
        co2_awarded=co2_saved                      
    )
    
    db.add(new_action)
    db.commit()
    db.refresh(new_action)

    return {"message": "Acción sostenible registrada con éxito", "action_id": new_action.id, "points_earned": points_earned}