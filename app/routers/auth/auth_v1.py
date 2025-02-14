from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.schemas.user_schema import LoginRequestSchema, SendOtpRequestSchema
from app.config import get_db
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not Found"}}
)


@router.post(path="/send-otp", summary="Login a user",
             description="Authentication of a user. Returns a JWT Token")
async def login(user: SendOtpRequestSchema, db: Session = Depends(get_db)):

    AuthService.send_otp(ph_no=user.mobile_number, db=db)

    return {"Message: ": "OTP generated successfully"}


@router.post(path="/login", summary="Login a user",
             description="Authentication of a user. Returns a JWT Token")
async def login(login_info: LoginRequestSchema,  db: Session = Depends(get_db) ):

    logged_in_data = AuthService.verify_otp(mobile_number=login_info.mobile_number,
                           otp=login_info.otp,
                           db=db)

    return {"Message: ": "Logged in Successfully",
            "data": logged_in_data
            }
