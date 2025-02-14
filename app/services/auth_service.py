import random
import string

from fastapi import HTTPException
from sqlalchemy.orm import Session
from twilio.rest import Client

from app.config import settings
from app.services.dal.auth_dal import AuthDal
from app.services.dal.user_dal import UserDal
from app.utils.jwt_utils import VxJWTUtils
from app.utils.twilio_utils import send_sms


def send_otp_twilio(phone_number: str, otp: str):
    account_sid = "your_account_sid"
    auth_token = "your_auth_token"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your OTP is {otp}. It is valid for 5 minutes.",
        from_="+your_twilio_number",
        to=phone_number
    )
    return message.sid


class AuthService:

    @staticmethod
    def send_otp(ph_no: str, db: Session):
        """
            Sending OTP for logging in
        """

        print("In Service Layer")

        user = UserDal.get_user_by_mobile(mobile_number=ph_no, db=db)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate a 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))

        print("OTP generated: ", otp)

        try:
            message_sid = None

            # Send OTP via Twilio
            if user.mobile_number == ph_no:
                pass
                # message_sid = send_sms(ph_no, otp)
                message_sid = "test123"

            # Todo check whether we need to send OTP to whatsapp number also?
            # integrate whatsapp OTP also
            # if user.whatsapp_number == ph_no:
            #     message_sid = send_sms(ph_no, otp)

        except Exception as e:
            raise HTTPException(status_code=500, detail="Twilio Exception")

        # Store OTP in the database (optional, for verification later)
        AuthDal.store_otp(db, ph_no, otp, message_sid)

        return {"message": "OTP sent successfully", "message_id": message_sid}

    @staticmethod
    def verify_otp(mobile_number: str, otp: str, db: Session):

        user = UserDal.get_user_by_mobile(db=db, mobile_number=mobile_number)

        if not AuthDal.verify_user_otp(db=db, user_id=user.id, otp=otp):
            raise HTTPException(400, "Invalid or Expired OTP provided")

        access_token = VxJWTUtils.create_access_token(
            data={
                "user_id": user.id,
                "login": True
            },
            expiry_delta=settings.access_token_expiry
        )

        return access_token
