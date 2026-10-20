from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.action_type_model import ActionLog
from app.core.levels import get_level_info  

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

    level_data = get_level_info(total_points)

    return {
        "total_points": total_points,
        "total_actions": total_actions,
        "total_co2_impact_kg": round(total_co2_impact, 2),
        "current_level": level_data["current_level"],
        "level_min": level_data.get("level_min", 0),
        "next_level": level_data.get("next_level"),
        "next_level_min": level_data.get("next_level_min"),
        "points_to_next": level_data.get("points_to_next"),
        "progress_percent": level_data.get("progress_percent", 100)
    }