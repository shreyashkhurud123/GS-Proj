from datetime import datetime, UTC
from typing import Optional
from sqlalchemy import ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.config import Base

class TimestampMixin:
    """
        Common class can be imported to get the below fields in the models.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC)  # Timezone-aware UTC timestamp
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        onupdate=lambda: datetime.now(UTC)  # Timezone-aware UTC timestamp on update
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )

    updated_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        ForeignKey('users.id')
    )


