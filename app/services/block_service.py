from sqlalchemy.orm import Session
from typing import List
from app.services.dal.dto.user_dto import UserDTO
from app.services.dal.role_dal import RoleDal
from app.services.dal.user_dal import UserDal
from app.services.dal.user_hierarchy_dal import DistrictDal
from app.schemas.block_schema import BlockAdminResponseSchema, BlockAdminUpdateResponse, BlockAdminUserSchema
from app.core.core_exceptions import NotFoundException, InvalidRequestException


class BlockService:
    @staticmethod
    def get_block_admins(db: Session) -> List[BlockAdminResponseSchema]:
        # Get Block Admin role first
        block_admin_role = RoleDal.get_role_by_name(db, "Block_Admin")
        if not block_admin_role:
            raise NotFoundException("Block Admin role not configured in system")

        print("Block Admin Role: ", block_admin_role.id, block_admin_role.name)

        districts = DistrictDal.get_all_districts(db)
        result = []

        for district in districts:
            # Get users with Block Admin role in this district
            admins = UserDal.get_users_by_role_and_district(
                db,
                role_id=block_admin_role.id,
                district_id=district.id
            )

            print("Admins: ", admins)

            result.append(BlockAdminResponseSchema(
                district_id=district.id,
                district_name=district.name,
                admin=BlockAdminUserSchema(
                    user_id=admins[0].id if admins else None,
                    user_name=f"{admins[0].first_name} {admins[0].last_name}" if admins else "No Admin"
                ) if admins else None
            ))

        return result

    @staticmethod
    def update_block_admin(db: Session, district_id: int, user_id: int, updated_by: int) -> BlockAdminUpdateResponse:
        # Validate district
        district = DistrictDal.get_district_by_id(db, district_id)
        if not district:
            raise NotFoundException(f"District with ID {district_id} not found")

        # Get user to be made admin
        user = UserDal.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            raise NotFoundException(f"Active user with ID {user_id} not found")

        # Verify user has Block Admin role
        if not UserDal.is_user_in_role(db, user_id, "Block_Admin"):
            raise InvalidRequestException("User must have Block Admin role to be assigned")

        # Update user's district assignment
        updated_user = UserDal.update_user(
            db=db,
            user_id=user_id,
            update_dict={
                "district_id": district_id,
                "block_id": None,  # Reset block assignment
                "updated_by": updated_by
            }
        )

        return BlockAdminUpdateResponse(
            success=True,
            message="Block admin updated successfully",
            admin_details=BlockAdminResponseSchema(
                district_id=district.id,
                district_name=district.name,
                admin=BlockAdminUserSchema(
                    user_id=updated_user.id,
                    user_name=f"{updated_user.first_name} {updated_user.last_name}"
                )
            )
        )




# # app/services/block_service.py
# from sqlalchemy.orm import Session
# from typing import List
# from app.services.dal.dto.user_dto import UserDTO
# from app.services.dal.user_dal import UserDal
# from app.services.dal.user_hierarchy_dal import DistrictDal
# from app.schemas.block_schema import BlockAdminResponseSchema, BlockAdminUpdateResponse, BlockAdminUserSchema
# from app.core.core_exceptions import NotFoundException, InvalidRequestException
#
#
# class BlockService:
#     @staticmethod
#     def get_block_admins(db: Session) -> List[BlockAdminResponseSchema]:
#         districts = DistrictDal.get_all_districts(db)
#         result = []
#
#         for district in districts:
#             # Get first active block admin for the district
#             admin = UserDal.get_users_by_designation_and_district(
#                 db,
#                 designation="BLOCK_ADMIN",
#                 district_id=district.id
#             )
#
#             result.append(BlockAdminResponseSchema(
#                 district_id=district.id,
#                 district_name=district.name,
#                 admin=BlockAdminUserSchema(
#                     user_id=admin[0].id if admin else None,
#                     user_name=f"{admin[0].first_name} {admin[0].last_name}" if admin else "No Admin"
#                 ) if admin else None
#             ))
#
#         return result
#
#     @staticmethod
#     def update_block_admin(db: Session, district_id: int, user_id: int, updated_by: int) -> BlockAdminUpdateResponse:
#         # Validate district
#         district = DistrictDal.get_district_by_id(db, district_id)
#         if not district:
#             raise NotFoundException(f"District with ID {district_id} not found")
#
#         # Get user to be made admin
#         user = UserDal.get_user_by_id(db, user_id)
#         if not user or not user.is_active:
#             raise NotFoundException(f"Active user with ID {user_id} not found")
#
#         # Verify user is already a block admin (optional business rule)
#         if user.designation != "BLOCK_ADMIN":
#             raise InvalidRequestException("User must be a block admin to be assigned to a district")
#
#         # Update user's district assignment
#         updated_user = UserDal.update_user(
#             db=db,
#             user_id=user_id,
#             update_dict={
#                 "district_id": district_id,
#                 "block_id": None,  # Reset block if needed
#                 "updated_by": updated_by
#             }
#         )
#
#         return BlockAdminUpdateResponse(
#             success=True,
#             message="Block admin updated successfully",
#             admin_details=BlockAdminResponseSchema(
#                 district_id=district.id,
#                 district_name=district.name,
#                 admin=BlockAdminUserSchema(
#                     user_id=updated_user.id,
#                     user_name=f"{updated_user.first_name} {updated_user.last_name}"
#                 )
#             )
#         )