from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ActionLog, ActionType
from ..schemas.catalog import ActionLogRead

router = APIRouter(
    prefix="/history",
    tags=["History"]
)

@router.get("", response_model=list[ActionLogRead])
def get_history(db: Session = Depends(get_db)):
    rows = db.execute(
        select(
            ActionLog.id,
            ActionLog.action_type_id,
            ActionLog.action_date,
            ActionLog.description,
            ActionLog.points_earned,
            ActionLog.co2_saved,
            ActionLog.category,
        )
        .join(ActionType, ActionType.id == ActionLog.action_type_id)
        .order_by(ActionLog.action_date.desc())
    ).all()

    return[
        ActionLogRead(
            id=r.id,
            action_type_id=r.action_type_id,
            action_date=r.action_date,
            description=r.description,
            points_earned=r.points_earned,
            co2_saved=r.co2_saved,
            category=r.category,
        )
        for r in rows
    ]