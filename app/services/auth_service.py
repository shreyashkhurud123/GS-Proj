import random
import string

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from twilio.rest import Client

from app.config import settings
from app.models.enums.user_designation import UserDesignation
from app.schemas.user_schema import UserRegisterRequest
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

    @staticmethod
    def register_user(user_data: UserRegisterRequest, db: Session):

        if UserDal.get_user_by_mobile(user_data.mobile_number, db):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with phone number {user_data.mobile_number} Already exists"
            )

        # TOdo add other validations

        # # Prepare user data for creation. Map payload keys to your model’s columns.
        # user_data = {
        #     "first_name": user_data.firstName,
        #     "last_name": user_data.lastName,
        #     "email": user_data.email,
        #     "mobile_number": user_data.mobile_number,
        #     "whatsapp_number": user_data.whatsAppMobileNumber,
        #     # For this example, we assume role_id is determined by designation.
        #     # You may adjust this logic as per your business rules.
        #     "role_id": 2,  # For instance, District_Admin role (id 2) by default.
        #     "designation": designation,
        #     "district_id": user_data.zillaParishadId,
        #     "block_id": user_data.panchayatSamitiId,
        #     "status": "APPROVED"  # Or set a default value as needed.
        # }

        UserDal.create_user(user_data, db)
        pass
