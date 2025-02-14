from datetime import datetime
from typing import Optional

from app.models.users import User


class UserDTO:
    def __init__(
            self,
            id: int,
            first_name: str,
            last_name: str,
            email: str,
            mobile_number: str,
            whatsapp_number: str,
            role_id: int,
            designation: str,
            district_id: Optional[int],
            block_id: Optional[int],
            gram_panchayat_id: Optional[int],
            status: str,
            # last_status_change: Optional[datetime],
            created_at: Optional[datetime],
            updated_at: Optional[datetime],
            created_by: int,
            updated_by: int,
            is_active: bool

    ):
        # User data
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mobile_number = mobile_number
        self.whatsapp_number = whatsapp_number
        self.role_id = role_id
        self.designation = designation
        self.district_id = district_id
        self.block_id = block_id
        self.gram_panchayat_id = gram_panchayat_id
        self.status = status
        # self.last_status_change = last_status_change

        # TimestampMixin cols
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by
        self.is_active = is_active

    @staticmethod
    def to_dto(user: User) -> "UserDTO":
        return UserDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            mobile_number=user.mobile_number,
            whatsapp_number=user.whatsapp_number,
            role_id=user.role_id,
            designation=user.designation,
            district_id=user.district_id,
            block_id=user.block_id,
            gram_panchayat_id=user.gram_panchayat_id,
            status=user.status,
            # last_status_change=user.last_status_change,
            created_at=user.created_at,
            updated_at=user.updated_by,
            created_by=user.created_by,
            updated_by=user.updated_by,
            is_active=user.is_active

        )
