from datetime import datetime, timezone, timedelta
from typing import Optional
from pytz import UTC

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.config import settings
from app.models.otp import UserOTP
from app.services.dal.dto.user_dto import UserDTO

from app.models.users import User


class UserDal:

    @staticmethod
    def get_user_by_mobile(mobile_number: str, db: Session) -> Optional[UserDTO]:
        """
            Getting UserDTO by Mobile
        """
        user = db.query(User).filter(and_(
            User.is_active,
            # Todo check what other parameters
            # User.
            or_(
                User.mobile_number == mobile_number,
                User.whatsapp_number == mobile_number

            ))).first()

        if user:
            return UserDTO.to_dto(user)

        return None

    @staticmethod
    def store_otp(db: Session, mobile_number: str, otp: str, message_sid: str) -> None:
        """
            Storing OTP for the user with the OTP current time
            Only One OTP record will be present per User
        """

        # using the get user just for defensive programming strategy
        user = UserDal.get_user_by_mobile(db=db, mobile_number=mobile_number)

        if not user:
            raise Exception("User not found for OTP storage.")

        expires_at = datetime.now(UTC) + timedelta(minutes=settings.otp_expiry_time)

        # Look for an existing OTP entry for the user.
        otp_record = db.query(UserOTP).filter(UserOTP.user_id == user.id).first()

        # If user already has an entry in the OTP table, OTP will be updated
        if otp_record:
            # Update the existing OTP record.
            otp_record.otp = otp
            otp_record.expires_at = expires_at
            otp_record.message_sid = message_sid

        else:
            # Create a new OTP record.
            otp_record = UserOTP(
                user_id=user.id,
                otp=otp,
                expires_at=expires_at,
                message_sid=message_sid
            )

            db.add(otp_record)

        # Commit the changes and refresh the record.
        db.commit()
        db.refresh(otp_record)
