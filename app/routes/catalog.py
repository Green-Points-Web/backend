from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.action_type_model import ActionType
from app.schemas.catalog import ActionTypeRead, ActionTypeUpdate


router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("", response_model=list[ActionTypeRead])
def list_catalog(
    active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = select(ActionType).order_by(ActionType.id)

    if active is not None:
        query = query.where(ActionType.active == active)

    return db.scalars(query).all()


@router.put("/{action_type_id}", response_model=ActionTypeRead)
def update_catalog_action(
    action_type_id: int,
    payload: ActionTypeUpdate,
    db: Session = Depends(get_db),
):
    action_type = db.get(ActionType, action_type_id)
    if action_type is None:
        raise HTTPException(status_code=404, detail="La acción no existe en el catálogo.")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=422,
            detail="Debe enviar al menos un campo para actualizar.",
        )
    if any(value is None for value in updates.values()):
        raise HTTPException(
            status_code=422,
            detail="Los campos de la acción no pueden ser nulos.",
        )

    if "name" in updates:
        existing_id = db.scalar(
            select(ActionType.id).where(
                ActionType.name == updates["name"],
                ActionType.id != action_type_id,
            )
        )
        if existing_id is not None:
            raise HTTPException(
                status_code=409,
                detail="Ya existe una acción con ese nombre.",
            )

    for field, value in updates.items():
        setattr(action_type, field, value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe una acción con ese nombre.",
        ) from exc

    db.refresh(action_type)
    return action_type