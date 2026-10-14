from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ActionTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    points: int
    co2_kg: float
    active: bool


class ActionLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action_type_id: int
    action_date: date
    description: Optional[str]
    points_earned: int
    co2_saved: float
    category: str
