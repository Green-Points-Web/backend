from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ActionType

CATALOG = [
    {"name": "Ir andando al trabajo", "category": "Movilidad", "points": 10, "co2_kg": 2.0},
    {"name": "Utilizar transporte público", "category": "Movilidad", "points": 10, "co2_kg": 1.0},
    {"name": "Ir en bicicleta", "category": "Movilidad", "points": 15, "co2_kg": 2.0},
    {"name": "Compartir coche", "category": "Movilidad", "points": 20, "co2_kg": 1.5},
    {"name": "Reciclar", "category": "Reciclaje", "points": 5, "co2_kg": 1.0},
    {"name": "Plantar un árbol", "category": "Naturaleza", "points": 50, "co2_kg": 10.0},
    {"name": "Participar en voluntariado ambiental", "category": "Participación", "points": 100, "co2_kg": 15.0},
]


def seed_catalog(db: Session) -> None:
    """Inserta las acciones del catálogo que aún no existan."""
    existing = set(db.scalars(select(ActionType.name)))
    new_actions = [ActionType(**item) for item in CATALOG if item["name"] not in existing]
    db.add_all(new_actions)
    db.commit()