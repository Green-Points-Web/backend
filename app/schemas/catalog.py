import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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
    action_date: datetime.date
    description: Optional[str]
    points_earned: int
    co2_saved: float
    category: str


class ActionLogUpdate(BaseModel):
    date: Optional[datetime.date] = None
    description: Optional[str] = Field(default=None, max_length=255)
