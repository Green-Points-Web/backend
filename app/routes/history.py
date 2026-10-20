from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.action_type_model import ActionLog, ActionType
from ..schemas.catalog import ActionLogRead, ActionLogUpdate


router = APIRouter(
    prefix="/history",
    tags=["History"],
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
    stmt = (
        select(
            ActionLog.id,
            ActionLog.action_type_id,
            ActionLog.date.label("action_date"),
            ActionLog.description,
            ActionLog.points_awarded.label("points_earned"),
            ActionLog.co2_awarded.label("co2_saved"),
            ActionLog.category.label("category"),
        )
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

    if order == "desc":
        sort = ActionLog.date.desc()
    else:
        sort = ActionLog.date.asc()

    stmt = stmt.order_by(sort, ActionLog.id.desc())
    stmt = stmt.limit(limit).offset(offset)

    rows = db.execute(stmt).all()

    return [
        ActionLogRead(
            id=row.id,
            action_type_id=row.action_type_id,
            action_date=row.action_date,
            description=row.description,
            points_earned=row.points_earned,
            co2_saved=row.co2_saved,
            category=row.category,
        )
        for row in rows
    ]

@router.put("/{action_id}")
def update_history_action(
    action_id: int,
    payload: ActionLogUpdate,
    db: Session = Depends(get_db),
):
    action = db.get(ActionLog, action_id)

    if action is None:
        raise HTTPException(status_code=404, detail="La acción no existe.")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=422,
            detail="Debe enviar al menos un campo para actualizar.",
        )

    non_nullable_fields = {
        "action_type_id",
        "action_date",
        "category",
        "points_earned",
        "co2_saved",
    }
    if any(updates[field] is None for field in non_nullable_fields if field in updates):
        raise HTTPException(
            status_code=422,
            detail="Los campos de la acción no pueden ser nulos.",
        )

    if "action_type_id" in updates and db.get(ActionType, updates["action_type_id"]) is None:
        raise HTTPException(
            status_code=404,
            detail="El tipo de acción no existe en el catálogo.",
        )

    if "action_date" in updates:
        if updates["action_date"] > date.today():
            raise HTTPException(
                status_code=400,
                detail="La fecha de la acción no puede ser futura.",
            )

    field_mapping = {
        "action_type_id": "action_type_id",
        "action_date": "date",
        "description": "description",
        "category": "category",
        "points_earned": "points_awarded",
        "co2_saved": "co2_awarded",
    }
    for field, value in updates.items():
        setattr(action, field_mapping[field], value)

    db.commit()
    db.refresh(action)
    return {
        "id": action.id,
        "action_type_id": action.action_type_id,
        "action_date": action.date,
        "description": action.description,
        "category": action.category,
        "points_earned": action.points_awarded,
        "co2_saved": action.co2_awarded,
    }


@router.delete("/{action_id}", status_code=204)
def delete_history_action(action_id: int, db: Session = Depends(get_db)):
    action = db.get(ActionLog, action_id)

    if action is None:
        raise HTTPException(status_code=404, detail="La acción no existe.")
    db.delete(action)
    db.commit()
    return None