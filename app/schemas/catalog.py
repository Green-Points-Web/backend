from pydantic import BaseModel, ConfigDict


class ActionTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    points: int
    co2_kg: float
    active: bool