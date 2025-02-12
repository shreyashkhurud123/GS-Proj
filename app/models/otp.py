from datetime import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.users import User

from app.config import Base


class UserOTP(Base):
    __tablename__ = "user_otps"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    otp: Mapped[str] = mapped_column(String(6), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    message_sid: Mapped[str] = mapped_column(String(50), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="otps", uselist=False)

