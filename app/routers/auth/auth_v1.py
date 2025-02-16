from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.schemas.user_schema import LoginRequestSchema, SendOtpRequestSchema, MessageResponse, UserRegisterRequest
from app.config import get_db
from app.services.auth_service import AuthService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not Found"}}
)


# This is how we are explicitly setting up the permissions for routers
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/send-otp', perm=VxAPIPermsEnum.PUBLIC)
@router.post(path="/send-otp", summary="Login a user",
             description="Authentication of a user. Returns a JWT Token")
async def login(user: SendOtpRequestSchema, db: Session = Depends(get_db)):
    AuthService.send_otp(ph_no=user.mobile_number, db=db)

    # return {"Message: ": "OTP generated successfully"}
    return MessageResponse(message="OTP generated successfully")


VxAPIPermsUtils.set_perm_post(path=router.prefix + '/login', perm=VxAPIPermsEnum.PUBLIC)
@router.post(path="/login", summary="Login a user",
             description="Authentication of a user. Returns a JWT Token")
async def login(login_info: LoginRequestSchema, db: Session = Depends(get_db)):
    logged_in_data = AuthService.verify_otp(mobile_number=login_info.mobile_number,
                                            otp=login_info.otp,
                                            db=db)

    return {"Message: ": "Logged in Successfully",
            "data": logged_in_data
            }


VxAPIPermsUtils.set_perm_post(path=router.prefix + '/register', perm=VxAPIPermsEnum.PUBLIC)
@router.post("/register", response_model=MessageResponse, description="Registering Gram Sevak User ")
def register_user(user_data: UserRegisterRequest, db: Session = Depends(get_db)):

    AuthService.register_user(user_data=user_data, db=db)

    return MessageResponse(message="User registration successful")
