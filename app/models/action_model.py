import datetime
from typing import Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class ActionType(Base):
    """Catálogo de acciones sostenibles."""

    __tablename__ = "action_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    co2_kg: Mapped[float] = mapped_column(Float, nullable=False)
    # Desactivar una acción NO borra su historial
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    logs: Mapped[list["ActionLog"]] = relationship(back_populates="action_type")


class ActionLog(Base):
    """Acciones registradas por el usuario (historial)."""

    __tablename__ = "action_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    action_type_id: Mapped[int] = mapped_column(
        ForeignKey("action_types.id"), nullable=False
    )
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # Snapshot: valores del catálogo en el momento del registro.
    # Así el historial no cambia si el catálogo se modifica después.
    points_awarded: Mapped[int] = mapped_column(Integer, nullable=False)
    co2_awarded: Mapped[float] = mapped_column(Float, nullable=False)

    action_type: Mapped["ActionType"] = relationship(back_populates="logs")
    