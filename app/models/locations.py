from sqlalchemy import (
    Integer, String, Float, DateTime, Boolean
)
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime
from .base import IDMixin, TimeStampMixin


class Location(Base, IDMixin, TimeStampMixin):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    month: Mapped[int]
    day: Mapped[int | None]

    country: Mapped[str]
    region: Mapped[str]
    province: Mapped[str | None]
    city: Mapped[str | None]
    location: Mapped[str | None]

    latitude: Mapped[float]
    longitude: Mapped[float]

    attack_type: Mapped[str]
    target: Mapped[str]
    description: Mapped[str | None]
    suicide_bombing: Mapped[bool]

    date_created: Mapped[datetime] = mapped_column(default=datetime.utcnow)
