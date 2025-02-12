from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Base
from app.models.base import TimestampMixin


class District(Base, TimestampMixin):
    __tablename__ = 'districts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    blocks: Mapped[List["Block"]] = relationship(back_populates="district")


class Block(Base, TimestampMixin):
    __tablename__ = 'blocks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    district_id: Mapped[int] = mapped_column(ForeignKey('districts.id'))

    district: Mapped["District"] = relationship(back_populates="blocks")
    gram_panchayats: Mapped[List["GramPanchayat"]] = relationship(back_populates="block")


class GramPanchayat(Base, TimestampMixin):
    __tablename__ = 'gram_panchayats'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.id'))

    block: Mapped["Block"] = relationship(back_populates="gram_panchayats")