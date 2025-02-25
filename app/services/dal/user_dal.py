from typing import Optional, List

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from app.models.enums.approval_status import ApprovalStatus
from app.models.enums.user_designation import UserDesignation
from app.models.users import User
from app.services.dal.dto.user_dto import UserDTO
from app.services.dal.role_dal import RoleDal


class UserDal:

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserDTO]:
        user = db.query(User).filter(
            User.id == user_id,
            User.is_active
        ).first()
        return UserDTO.to_dto(user) if user else None

    @staticmethod
    def get_users_by_role(db: Session, role_id: int) -> List[UserDTO]:
        users = db.query(User).filter(
            User.role_id == role_id,
            User.is_active,
            User.status == ApprovalStatus.APPROVED
        ).all()
        return [UserDTO.to_dto(user) for user in users] if users else []

    @staticmethod
    def update_user(db: Session, user_id: int, update_dict: dict) -> UserDTO:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        for key, value in update_dict.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return UserDTO.to_dto(user)

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

    @staticmethod
    def get_users_by_role_and_district(db: Session, role_id: int, district_id: int) -> List[UserDTO]:

        print("In DAL:", role_id, district_id)

        users = db.query(User).filter(
            User.role_id == role_id,
            User.district_id == district_id,
            User.is_active,
            User.status == ApprovalStatus.APPROVED
        ).all()

        return [UserDTO.to_dto(user) for user in users] if users else []

    @staticmethod
    def is_user_in_role(db: Session, user_id: int, role_name: str) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        role = RoleDal.get_role_by_name(db, role_name)
        return user.role_id == role.id if role else False