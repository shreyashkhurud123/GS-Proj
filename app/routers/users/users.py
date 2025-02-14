from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.schemas.user_schema import LoginRequestSchema, SendOtpRequestSchema
from app.config import get_db
from app.services.auth_service import AuthService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/user",
    tags=["user"],
    responses={404: {"description": "Not Found"}}
)

