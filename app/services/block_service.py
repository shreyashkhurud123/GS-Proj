from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.dal.dto.user_dto import UserDTO
from app.services.dal.role_dal import RoleDal
from app.services.dal.user_dal import UserDal
from app.services.dal.user_hierarchy_dal import DistrictDal, BlockDal
from app.schemas.block_schema import BlockAdminResponseSchema, BlockAdminUpdateResponse, BlockAdminUserSchema
from app.core.core_exceptions import NotFoundException, InvalidRequestException


class BlockService:
    @staticmethod
    def get_block_admins(db: Session, search_term: Optional[str]) -> List[BlockAdminResponseSchema]:
        """
            Getting all the block admins which belongs to the blocks matching the provided search term
        """
        # Get Block Admin role first
        block_admin_role = RoleDal.get_role_by_name(db, "Block_Admin")
        if not block_admin_role:
            raise NotFoundException("Block Admin role not configured in system")

        print("Block Admin Role: ", block_admin_role.id, block_admin_role.name)

        districts = DistrictDal.get_all_districts(db)
        result = []

        print("search term: ", search_term)

        if search_term:
            block_ids = [b.id for b in BlockDal.get_blocks_by_search_term(db=db, search_term=search_term)]
        else:
            block_ids = [b.id for b in BlockDal.get_all_active_blocks(db=db)]

        print("Blocks are: ", block_ids)

        for district in districts:
            # Get users with Block Admin role in this district
            admins = [admin for admin in UserDal.get_users_by_role_and_district(
                db,
                role_id=block_admin_role.id,
                district_id=district.id
            # )]
            ) if admin.block_id in block_ids]

            print("Admins blocks", [admin.id for admin in admins])

            print("Admins: ", admins)

            result.append(BlockAdminResponseSchema(
                block_id=district.id,
                block_name=district.name,
                admin=BlockAdminUserSchema(
                    user_id=admins[0].id if admins else None,
                    user_name=f"{admins[0].first_name} {admins[0].last_name}" if admins else "No Admin"
                ) if admins else None
            ))

        return result

    @staticmethod
    def update_block_admin(db: Session, block_id: int,
                           user_id: int, updated_by: int) -> BlockAdminUpdateResponse:
        # Checking if block exists
        block = BlockDal.get_block_by_id(db, block_id)

        if not block:
            raise NotFoundException(f"block with ID {block_id} not found")

        # Checking if user exists
        user = UserDal.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            raise NotFoundException(f"Active user with ID {user_id} not found")

        # Checking if user belongs to provided block
        # Todo check whether we need below condition
        if user.block_id != block_id:
            raise InvalidRequestException(f"User {user_id} does not belong to {block_id}")

        # Updating the role for user to block admin
        updated_user = UserDal.update_user(
            db=db,
            user_id=user_id,
            update_dict={
                "role_id": 3,
                "block_id": block_id,
                "updated_by": updated_by
            }
        )

        return BlockAdminUpdateResponse(
            success=True,
            message="Block admin updated successfully",
            admin_details=BlockAdminResponseSchema(
                block_id=block.id,
                block_name=block.name,
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
