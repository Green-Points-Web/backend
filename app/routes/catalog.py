from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.catalog import ActionTypeRead, ActionTypeUpdate
from app.controller import catalog_controller

router = APIRouter(prefix="/catalog", tags=["Catalog"])

@router.get("", response_model=list[ActionTypeRead])
def list_catalog(
    active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    return catalog_controller.get_catalog(db=db, active=active)


@router.put("/{action_type_id}", response_model=ActionTypeRead)
def update_catalog_action(
    action_type_id: int,
    payload: ActionTypeUpdate,
    db: Session = Depends(get_db),
):
    return catalog_controller.update_action_in_catalog(db=db, action_type_id=action_type_id, payload=payload)