import random
import string

from fastapi import HTTPException
from sqlalchemy.orm import Session
from twilio.rest import Client
from app.services.dal.user_dal import UserDal
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

        user = UserDal.get_user_by_mobile(mobile_number=ph_no, db=db)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate a 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))

        try:
            message_sid = None

            # Send OTP via Twilio
            if user.mobile_number == ph_no:
                message_sid = send_sms(ph_no, otp)

            # Todo check whether we need to send OTP to whatsapp number also?
            # integrate whatsapp OTP also
            # if user.whatsapp_number == ph_no:
            #     message_sid = send_sms(ph_no, otp)

        except Exception as e:
            raise HTTPException(status_code=500, detail="Twilio Exception")

        # Store OTP in the database (optional, for verification later)
        UserDal.store_otp(db, ph_no, otp, message_sid)

        return {"message": "OTP sent successfully", "message_id": message_sid}
