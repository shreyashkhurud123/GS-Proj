from pydantic import BaseModel


class BlockAdminUserSchema(BaseModel):
    user_id: int
    user_name: str


class BlockAdminResponseSchema(BaseModel):
    district_id: int
    district_name: str
    admin: BlockAdminUserSchema

    # Check below and add
    # class Config:
    #     json_encoders = {
    #         int: lambda v: str(v),  # Convert IDs to strings if needed
    #     }


class BlockAdminUpdateRequest(BaseModel):
    district_id: int
    admin: BlockAdminUserSchema  # Reuse previous schema


class BlockAdminUpdateResponse(BaseModel):
    success: bool
    message: str
    admin_details: BlockAdminResponseSchema

