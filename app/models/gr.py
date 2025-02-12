from datetime import date
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.config import Base
from app.models.base import TimestampMixin


class Yojana(Base, TimestampMixin):
    __tablename__ = 'yojanas'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    # Todo not needed
    # department: Mapped[str] = mapped_column(String(100))
    # grs: Mapped[List["GR"]] = relationship(back_populates="yojana")


class GR(Base, TimestampMixin):
    __tablename__ = 'grs'

    id: Mapped[int] = mapped_column(primary_key=True)
    gr_number: Mapped[str] = mapped_column(String(50), unique=True)
    gr_code: Mapped[Optional[str]] = mapped_column(String(50), unique=True)

    # Todo table for department and fk id from dept table
    department_name: Mapped[str] = mapped_column(String(100))
    effective_date: Mapped[date] = mapped_column(Date)
    yojana_id: Mapped[int] = mapped_column(ForeignKey('yojanas.id'))
    file_path: Mapped[str] = mapped_column(String(500))

    yojana: Mapped["Yojana"] = relationship(back_populates="grs")