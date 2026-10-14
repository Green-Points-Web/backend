from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.action_type_model import ActionType
from app.schemas.catalog import ActionTypeRead


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