from datetime import date
from sqlalchemy import String, Date, ForeignKey, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from app.config import Base
from app.models.base import TimestampMixin


class Yojana(Base, TimestampMixin):
    __tablename__ = 'yojanas'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    grs: Mapped[List["GR"]] = relationship("GR", back_populates="yojana")

    # Todo not needed
    # department: Mapped[str] = mapped_column(String(100))
    # grs: Mapped[List["GR"]] = relationship(back_populates="yojana")


class GR(Base, TimestampMixin):
    __tablename__ = 'grs'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gr_number: Mapped[str] = mapped_column(String(50), unique=True)
    gr_code: Mapped[Optional[str]] = mapped_column(String(50), unique=True)

    # Todo table for department and fk id from dept table
    department_name: Mapped[str] = mapped_column(String(100),index=True)
    effective_date: Mapped[date] = mapped_column(Date,index=True)
    yojana_id: Mapped[int] = mapped_column(ForeignKey('yojanas.id'))
    file_path: Mapped[str] = mapped_column(String(500))

    yojana: Mapped["Yojana"] = relationship("Yojana", back_populates="grs")

    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )

    updated_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )

    yojana: Mapped["Yojana"] = relationship("Yojana", back_populates="grs")

    __table_args__ = (
        Index('ix_gr_department_effective_date', 'department_name', 'effective_date'),
    )
