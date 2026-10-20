import datetime
from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ActionTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    points: int
    co2_kg: float
    active: bool


class ActionTypeUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    points: Optional[int] = Field(default=None, gt=0)
    co2_kg: Optional[float] = Field(default=None, ge=0)


class ActionLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action_type_id: int
    action_date: datetime.date
    description: Optional[str]
    points_earned: int
    co2_saved: float
    category: str
    cancelled: bool = False
    annulled: bool = False
    status: str = "active"


class ActionLogUpdate(BaseModel):
    action_type_id: Optional[int] = Field(default=None, gt=0)
    action_date: Optional[datetime.date] = Field(
        default=None,
        validation_alias=AliasChoices("action_date", "date"),
    )
    description: Optional[str] = Field(default=None, max_length=255)
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    points_earned: Optional[int] = Field(default=None, gt=0)
    co2_saved: Optional[float] = Field(default=None, ge=0)
    cancelled: Optional[bool] = None
    status: Optional[str] = None