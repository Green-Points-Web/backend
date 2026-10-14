
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.action_type_model import ActionLog

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
def get_dashboard(db: Session = Depends(get_db)):
    summary = db.execute(
        select(
            func.coalesce(
                func.sum(ActionLog.points_awarded), 0
            ).label("total_points"),
            func.count(ActionLog.id).label("total_actions"),
            func.coalesce(
                func.sum(ActionLog.co2_awarded), 0.0
            ).label("total_co2_impact"),
        )
    ).one()

    total_points = summary.total_points
    total_actions = summary.total_actions
    total_co2_impact = summary.total_co2_impact

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
