from datetime import datetime

from sqlalchemy import String, Enum as SQAEnum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from app.config import Base
from app.models.base import TimestampMixin
from app.models.enums.user_designation import UserDesignation

from app.models.enums.status import Status


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    # Todo check what all cols to make mandatory
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    mobile_number: Mapped[str] = mapped_column(String(15), unique=True)
    whatsapp_number: Mapped[Optional[str]] = mapped_column(String(15), unique=True)

    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    # Todo check proper names
    designation: Mapped["UserDesignation"] = mapped_column(SQAEnum(UserDesignation))

    district_id: Mapped[Optional[int]] = mapped_column(ForeignKey('districts.id'))
    block_id: Mapped[Optional[int]] = mapped_column(ForeignKey('blocks.id'))
    gram_panchayat_id: Mapped[Optional[int]] = mapped_column(ForeignKey('gram_panchayats.id'))

    status: Mapped[Status] = mapped_column(
        SQAEnum(Status),
        default=Status.PENDING
    )

    # last_status_change: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # Relations
    role: Mapped["Role"] = relationship(back_populates="users")
    documents: Mapped[List["UserDocument"]] = relationship(back_populates="user")

    # Storing list of OTP's for user
    # otps: Mapped[List["UserOTP"]] = relationship("UserOTP", back_populates="user")
    # For now storing OTP's for user as single entry only instead of List of OTPs
    otps: Mapped["UserOTP"] = relationship("UserOTP", back_populates="user")
