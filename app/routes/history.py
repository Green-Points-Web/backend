from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.action_type_model import ActionLog, ActionType
from ..schemas.catalog import ActionLogRead, ActionLogUpdate


router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=list[ActionLogRead])
def get_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    action_type_id: Optional[int] = None,
    min_points: Optional[int] = None,
    include_cancelled: bool = Query(True),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(1000, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(ActionLog)
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
    if not include_cancelled:
        stmt = stmt.where(ActionLog.cancelled == False)

    sort = ActionLog.date.desc() if order == "desc" else ActionLog.date.asc()
    rows = db.scalars(stmt.order_by(sort, ActionLog.id.desc()).limit(limit).offset(offset)).all()

    result = []
    for action in rows:
        result.append(
            ActionLogRead(
                id=action.id,
                action_type_id=action.action_type_id,
                action_date=action.date,
                description=action.description,
                points_earned=action.points_awarded,
                co2_saved=action.co2_awarded,
                category=action.category,
                cancelled=action.cancelled,
                annulled=action.cancelled,
                status="cancelled" if action.cancelled else "active",
            )
        )
    return result


@router.put("/{action_id}", response_model=ActionLogRead)
def update_history_action(action_id: int, payload: ActionLogUpdate, db: Session = Depends(get_db)):
    action = db.get(ActionLog, action_id)
    if action is None:
        raise HTTPException(status_code=404, detail="La acción no existe.")

    updates = payload.model_dump(exclude_unset=True)

    if "action_date" in updates and updates["action_date"] is not None:
        if updates["action_date"] > date.today():
            raise HTTPException(status_code=400, detail="La fecha de la acción no puede ser futura.")
        action.date = updates["action_date"]

    if "date" in updates and updates["date"] is not None:
        if updates["date"] > date.today():
            raise HTTPException(status_code=400, detail="La fecha de la acción no puede ser futura.")
        action.date = updates["date"]

    if "action_type_id" in updates and updates["action_type_id"] is not None:
        action_type = db.get(ActionType, updates["action_type_id"])
        if action_type is None:
            raise HTTPException(status_code=404, detail="El tipo de acción seleccionada no existe en el catálogo.")
        action.action_type_id = action_type.id
        if "category" not in updates:
            action.category = action_type.category
        if "points_earned" not in updates:
            action.points_awarded = action_type.points
        if "co2_saved" not in updates:
            action.co2_awarded = action_type.co2_kg

    if "description" in updates:
        action.description = updates["description"]

    if "category" in updates and updates["category"] is not None:
        action.category = updates["category"]

    if "points_earned" in updates and updates["points_earned"] is not None:
        action.points_awarded = updates["points_earned"]

    if "co2_saved" in updates and updates["co2_saved"] is not None:
        action.co2_awarded = updates["co2_saved"]

    if "cancelled" in updates and updates["cancelled"] is not None:
        action.cancelled = updates["cancelled"]

    if "status" in updates and updates["status"] is not None:
        action.cancelled = str(updates["status"]).lower() in {"cancelled", "anulled", "inactive", "void"}

    db.commit()
    db.refresh(action)

    return ActionLogRead(
        id=action.id,
        action_type_id=action.action_type_id,
        action_date=action.date,
        description=action.description,
        points_earned=action.points_awarded,
        co2_saved=action.co2_awarded,
        category=action.category,
        cancelled=action.cancelled,
        annulled=action.cancelled,
        status="cancelled" if action.cancelled else "active",
    )


@router.delete("/{action_id}", status_code=204)
def annul_history_action(action_id: int, db: Session = Depends(get_db)):
    action = db.get(ActionLog, action_id)
    if action is None:
        raise HTTPException(status_code=404, detail="La acción no existe.")
    action.cancelled = True
    db.commit()
    return None


@router.post("/{action_id}/annul", status_code=200)
def annul_history_action_post(action_id: int, db: Session = Depends(get_db)):
    action = db.get(ActionLog, action_id)
    if action is None:
        raise HTTPException(status_code=404, detail="La acción no existe.")
    action.cancelled = True
    db.commit()
    db.refresh(action)
    return ActionLogRead(
        id=action.id,
        action_type_id=action.action_type_id,
        action_date=action.date,
        description=action.description,
        points_earned=action.points_awarded,
        co2_saved=action.co2_awarded,
        category=action.category,
        cancelled=action.cancelled,
        annulled=action.cancelled,
        status="cancelled" if action.cancelled else "active",
    )


@router.patch("/{action_id}/annul", status_code=200)
def annul_history_action_patch(action_id: int, db: Session = Depends(get_db)):
    return annul_history_action_post(action_id, db)