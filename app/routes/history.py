from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.action_type_model import ActionLog
from ..schemas.catalog import ActionLogRead

router = APIRouter(
    prefix="/history",
    tags=["History"]
)

@router.get("", response_model=list[ActionLogRead])

def get_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    action_type_id: Optional[int] = None,
    min_points: Optional[int] = None,
    order: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(
        ActionLog.id,
        ActionLog.action_type_id,
        ActionLog.date.label("action_date"),
        ActionLog.description,
        ActionLog.points_awarded.label("points_earned"),
        ActionLog.co2_awarded.label("co2_saved"),
        ActionLog.category,
    )

    if start_date is not None:
        stmt = stmt.where(ActionLog.date >= start_date)
    if end_date is not None:
        stmt = stmt.where(ActionLog.date <= end_date)
    if category is not None:
        stmt = stmt.where(ActionLog.category == category)
    if action_type_id is not None:
        stmt = stmt.where(ActionLog.action_type_id == action_type_id)
    if min_points is not None:
        stmt = stmt.where(ActionLog.points_awarded >= min_points)

    sort = ActionLog.date.desc() if order == "desc" else ActionLog.date.asc()
    stmt = stmt.order_by(sort, ActionLog.id.desc()).limit(limit).offset(offset)

    rows = db.execute(stmt).all()

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