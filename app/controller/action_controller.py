from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.models.action_type_model import ActionType, ActionLog
from app.schemas.schemas import ActionCreate

def create_action_log(db: Session, action_data: ActionCreate):
    action_date_value = action_data.action_date
    if action_date_value > date.today():
        raise HTTPException(status_code=400, detail="La fecha de la acción no puede ser en el futuro.")

    action_type_id = action_data.action_type_id
    action_type = db.query(ActionType).filter(ActionType.id == action_type_id).first()
    
    if not action_type:
        raise HTTPException(status_code=404, detail="El tipo de acción seleccionada no existe en el catálogo.")

    points_earned = action_type.points
    co2_saved = action_type.co2_kg  

    new_action = ActionLog(
        action_type_id=action_type.id,
        date=action_date_value,
        category=action_type.category,
        description=action_data.description,
        points_awarded=points_earned,
        co2_awarded=co2_saved
    )
    
    db.add(new_action)
    db.commit()
    db.refresh(new_action)

    return {"message": "Acción sostenible registrada con éxito", "action_id": new_action.id, "points_earned": points_earned}