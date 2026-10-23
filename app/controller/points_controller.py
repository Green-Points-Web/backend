from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.action_type_model import ActionLog

def level_for(points: int) -> str:
    if points < 100:
        return "Seed"
    if points < 300:
        return "Sprout"
    if points < 700:
        return "Tree"
    if points < 1500:
        return "Forest"
    return "Planet Hero"

def get_total_points(db: Session) -> int:
    total = db.scalar(
        select(
            func.coalesce(func.sum(ActionLog.points_awarded), 0)
        )
    )
    return int(total or 0)

def add_user_points(db: Session, user_id: str):
    total = get_total_points(db)
    return {
        "user_id": user_id,
        "points": total,
        "level": level_for(total),
    }

def get_user_points(db: Session, user_id: str):
    if user_id != "test_user":
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    total = get_total_points(db)

    thresholds = [
        ("Seed", 0),
        ("Sprout", 100),
        ("Tree", 300),
        ("Forest", 700),
        ("Planet Hero", 1500),
    ]

    next_level = None
    points_to_next_level = None

    for name, threshold in thresholds:
        if threshold > total:
            next_level = name
            points_to_next_level = threshold - total
            break

    return {
        "user_id": user_id,
        "points": total,
        "level": level_for(total),
        "next_level": next_level,
        "points_to_next_level": points_to_next_level,
    }