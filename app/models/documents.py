from sqlalchemy import String, Boolean, Enum as SQAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config import Base
from app.models.base import TimestampMixin
from typing import List, Optional
from app.models.enums.status import Status


class DocumentType(Base, TimestampMixin):

    """
        GramSevak Of pune Specific documents. Mandatory and non-mandatory
    """

    __tablename__ = 'document_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)


class UserDocument(Base, TimestampMixin):

    __tablename__ = 'user_documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    document_type_id: Mapped[int] = mapped_column(ForeignKey('document_types.id'))
    file_path: Mapped[str] = mapped_column(String(500))

    verification_status: Mapped[str] = mapped_column(
        # Todo create seperate enums instead of using directly
        SQAEnum(Status),
        # By default documents will be verified
        default=Status.APPROVED
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="documents")
    document_type: Mapped["DocumentType"] = relationship()
