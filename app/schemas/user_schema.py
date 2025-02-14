from typing import Optional

from pydantic import field_validator
from app.schemas.base import CamelModel
from pydantic import EmailStr, Field



class SendOtpRequestSchema(CamelModel):
    """
        Send OTP Request schema for getting otp.
        Here We are validating the mobile number
    """
    mobile_number: str

    @field_validator('mobile_number')
    def validate_mobile_number(cls, value: str) -> str:
        """
            This will validate whether the number starts with + or it has only numbers
            todo check req.
        """

        if not value.startswith('+91'):
            raise ValueError("Phone number must start with '+' and contain only digits")

        if not value[1:].isdigit():
            raise ValueError("Phone number must start with '+' and contain only digits")

        return value


class LoginRequestSchema(SendOtpRequestSchema):
    otp: str


class UserRegisterRequest(CamelModel):
    first_name: str
    last_name: str
    designation_id: int
    zilla_parishad_id: int
    panchayat_samiti_id: int
    mobile_number: str
    whatsapp_number: str
    # Todo check whether to keep optional
    email: Optional[EmailStr] = None


class MessageResponse(CamelModel):
    message: str



# from pydantic import BaseModel, field_validator, Field
# from typing import Optional, List
# from fastapi_camelcase import CamelModel
#
#
# # https://medium.com/analytics-vidhya/camel-case-models-with-fast-api-and-pydantic-5a8acb6c0eee
# # FrontEnd is Sending data in CamelCase.
# # When we return the data, it will be sent in Camel Case using below model
# class SendOtpRequsetSchema(CamelModel):
#     # mobile_number: str = Field(..., alias="mobileNumber")
#     mobile_number: str
#
#     @field_validator('mobile_number')
#     def validate_mobile_number(cls, value):
#
#         print("IN Validation: ", print(value))
#
#         if value and not value.startswith('+') and not value.isdigit():
#             raise ValueError("Phone number must start with '+' and contains only digits")
#
#
# class LoginRequestSchema(SendOtpRequsetSchema):
#     # mobile_number: str = Field(..., alias="mobileNumber")
#     otp: str
#
#
# # class LoginRequestSchema(CamelModel):
# #     user_id: int
# #     mobile_number: str
# #     otp: str
#
#
# class UserCreate(CamelModel):
#     firstName: str
#     lastName: str
#     designationId: int
#     zillaParishadId: int
#     panchayatSamitiId: int
#     mobileNumber: str
#     whatsAppMobileNumber: str
#     email: str
#
#
# class DocumentResponse(CamelModel):
#     # Todo check params
#     id: int
#     filename: str
#     is_admin_uploaded: bool
#
#     class Config:
#         orm_mode = True
