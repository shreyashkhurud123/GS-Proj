from typing import Optional

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from app.models.enums.approval_status import ApprovalStatus
from app.models.enums.user_designation import UserDesignation
from app.models.users import User
from app.services.dal.dto.user_dto import UserDTO


class UserDal:

    @staticmethod
    def get_user_by_mobile(mobile_number: str, db: Session) -> Optional[UserDTO]:
        """
            Getting UserDTO by Mobile
        """

        print("In user Dal")

        user = db.query(User).filter(and_(
            User.is_active,
            # Todo check what other parameters
            # User.
            or_(
                # Approach 1: We can Directly compare the mobile numbers
                #  This might give us a mismatch if either of the mobile number is having
                #  `+91` but the other doesn't
                # User.mobile_number == mobile_number,
                # User.whatsapp_number == mobile_number

                # This will check if the provided mobile number string is in the stored mobile number
                # But if the stored mobile number doesn't have `+91` this will fail. Hence check that
                User.mobile_number.like(mobile_number),
                User.whatsapp_number.like(mobile_number)

            ))).first()

        if user:
            return UserDTO.to_dto(user)

        return None

    @staticmethod
    def create_user(db: Session, first_name: str, last_name: str, email: str,
                    mobile_number: str, whatsapp_number: str,
                    gram_panchayat_id: int,
                    designation: UserDesignation, district_id: int, block_id: int,
                    status: ApprovalStatus, role_id: Optional[int] = 1):

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            whatsapp_number=whatsapp_number,
            designation=designation,
            district_id=district_id,
            block_id=block_id,
            gram_panchayat_id=gram_panchayat_id,
            status=status,
            role_id=role_id

        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
