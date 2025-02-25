from pydantic import BaseModel
from typing_extensions import List

from app.schemas.base import CamelModel


class BlockAdminUserSchema(CamelModel):
    user_id: int
    user_name: str


class BlockAdminResponseSchema(CamelModel):
    block_id: int
    block_name: str
    admin: BlockAdminUserSchema

    # Check below and add
    # class Config:
    #     json_encoders = {
    #         int: lambda v: str(v),  # Convert IDs to strings if needed
    #     }


class BlockAdminUpdateRequest(CamelModel):
    block_id: int
    user_id: int
    # admin: BlockAdminUserSchema


class BlockAdminUpdateResponse(CamelModel):
    success: bool
    message: str
    admin_details: BlockAdminResponseSchema

