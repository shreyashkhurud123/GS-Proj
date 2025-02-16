from sqlalchemy import String, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.config import Base
from app.models.base import TimestampMixin


class Book(Base, TimestampMixin):

    '''

    '''

    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)

    # Todo table for department and fk id from dept table
    department: Mapped[str] = mapped_column(String(100))
    file_path: Mapped[str] = mapped_column(String(500))

    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )

    updated_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )

    __table_args__ = (
        Index('ix_books_title', 'title'),
        Index('ix_books_department', 'department'),
    )

    # Not needed
    # category: Mapped[Optional[str]] = mapped_column(String(100))
