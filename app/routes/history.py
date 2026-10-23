from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.catalog import ActionLogRead, ActionLogUpdate
from app.controller import history_controller

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
    limit: Optional[int] = Query(None, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return history_controller.get_action_history(
        db=db,
        start_date=start_date,
        end_date=end_date,
        category=category,
        action_type_id=action_type_id,
        min_points=min_points,
        include_cancelled=include_cancelled,
        order=order,
        limit=limit,
        offset=offset
    )


@router.put("/{action_id}", response_model=ActionLogRead)
def update_history_action(action_id: int, payload: ActionLogUpdate, db: Session = Depends(get_db)):
    return history_controller.update_action_in_history(db=db, action_id=action_id, payload=payload)


@router.delete("/{action_id}", status_code=204)
def annul_history_action(action_id: int, db: Session = Depends(get_db)):
    return history_controller.annul_action_delete(db=db, action_id=action_id)


@router.post("/{action_id}/annul", status_code=200)
def annul_history_action_post(action_id: int, db: Session = Depends(get_db)):
    return history_controller.annul_action_status(db=db, action_id=action_id)


@router.patch("/{action_id}/annul", status_code=200)
def annul_history_action_patch(action_id: int, db: Session = Depends(get_db)):
    return history_controller.annul_action_status(db=db, action_id=action_id)