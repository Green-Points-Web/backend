
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.action_type_model import ActionLog

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
def get_dashboard(db: Session = Depends(get_db)):
    total_points = db.scalar(
        select(func.coalesce(func.sum(ActionLog.points_earned), 0))
    )

    total_actions = db.scalar(
        select(func.count(ActionLog.id))
    )

    total_co2_impact = db.scalar(
        select(func.coalesce(func.sum(ActionLog.co2_earned), 0.0))
    )

    if total_points < 100:
        current_level = "Seed"
    elif total_points < 300:
        current_level = "Sprout"
    elif total_points < 700:
        current_level = "Tree"
    elif total_points < 1500:
        current_level = "Forest"
    else:
        current_level = "Planet Hero"

    return {
        "total_points": total_points,
        "current_level": current_level,
        "total_actions": total_actions,
        "total_co2_impact_kg": round(total_co2_impact, 2),
    }
