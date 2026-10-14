from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date

class ActionTypeBase(BaseModel):
    name: str = Field(min_length=2, description="Action name")
    category: str = Field(min_length=1, description="Movilidad | Reciclaje | Naturaleza | Participacción")
    points: int = Field(gt=0, description="Points granted per registration")
    co2_impact: float = Field(ge=0, description="Kg of Co2 saved per registration")

class ActionTypeCreate(ActionTypeBase):
    pass

class ActionTypeResponse(ActionTypeBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class ActionBase(BaseModel):
    action_type_id: int = Field(gt=0, description="Catalog action id")
    action_date: date = Field(description="Valid date YYYY-MM-DD")
    description: Optional[str] = Field(default=None, max_length=500, description="Free text comment")

class ActionCreate(ActionBase):
    pass

class ActionResponse(BaseModel):
    id: int
    action_type_id: int
    action_date: date
    description: str
    points_earned: int
    co2_saved: float

    model_config = ConfigDict(from_attributes=True)