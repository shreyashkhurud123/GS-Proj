from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.core_exceptions import NotFoundException, InvalidRequestException
from app.models.enums.approval_status import ApprovalStatus, ApprovalStatusRequest
from app.schemas.gramsevak_schema import GramsevakListItem, GramsevakDetailResponse
from app.services.dal.document_dal import UserDocumentDal
from app.services.dal.user_hierarchy_dal import DistrictDal, BlockDal, GramPanchayatDal
from app.services.dal.role_dal import RoleDal
from app.services.dal.user_dal import UserDal


class GramsevakService:
    @staticmethod
    def get_gramsevak_list(
            db: Session,
            search_term: Optional[str] = None,
            status_filter: ApprovalStatusRequest= ApprovalStatusRequest.ALL
    ) -> List[GramsevakListItem]:

        gramsevak_role = RoleDal.get_role_by_name(db, "Gram_Sevak")
        if not gramsevak_role:
            raise NotFoundException("Gram Sevak role not found")

        users = UserDal.get_gramsevaks(
            db,
            role_id=gramsevak_role.id,
            search_term=search_term,
            status_filter=status_filter
        )

        result = []
        for user in users:
            district = DistrictDal.get_district_by_id(db, user.district_id)
            block = BlockDal.get_block_by_id(db, user.block_id)

            result.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "block": block.name if block else "N/A",
                "district": district.name if district else "N/A",
                "service_id": 'temp_service_id',
                "is_approved": user.status == "APPROVED"
            })

        return result

    @staticmethod
    def get_gramsevak_details(db: Session, gramsevak_id: int) -> GramsevakDetailResponse:

        user = UserDal.get_user_with_details_by_id(db, gramsevak_id)

        print("here 1 ")

        if not user or not user.role_id:
            raise InvalidRequestException("User Role not found")

        print("here 2 ")

        if RoleDal.get_role_by_name(db=db, name="Gram_Sevak").id != user.role_id:
            raise InvalidRequestException("User is not assigned as Gram Sevak")

        print("here 3 ")

        district = DistrictDal.get_district_by_id(db=db, district_id=user.district_id)
        block = BlockDal.get_block_by_id(db=db, block_id=user.block_id)
        gram_panchayat = GramPanchayatDal.get_gram_panchayat_by_id(db=db, gp_id=user.gram_panchayat_id)

        print("here 4 ")

        # documents = UserDocumentDal.get_user_documents(db, user.id)

        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "designation_name": user.designation.name,
            "district": {
                "district_id": district.id,
                "district_name": district.name
            },
            "block": {
                "block_id": block.id,
                "block_name": block.name
            },
            "gram_panchayat": {
                "gram_panchayat_id": gram_panchayat.id,
                "gram_panchayat_name": gram_panchayat.name
            },
            "mobile_number": user.mobile_number,
            "whatsapp_number": user.whatsapp_number,
            "email": user.email
            # "documents": [{
            #     "document_type": doc.document_type.name,
            #     "document_name": doc.document_type.name,
            #     "document_path": doc.file_path
            # } for doc in documents]
        }

    @staticmethod
    def update_gramsevak_status(
            db: Session,
            gramsevak_id: int,
            new_status: ApprovalStatus
    ):

        user = UserDal.get_user_by_id(db, gramsevak_id)

        if not user or not user.role_id:
            raise NotFoundException("Gramsevak not found")

        if not RoleDal.get_role_by_name(db=db, name="Gram_Sevak").id != user.role_id:
            raise NotFoundException("Role id not found")

        print("Calling DAL")

        UserDal.update_user(
            db,
            user_id=gramsevak_id,
            update_dict={"status": new_status}
        )

        return {"message": "Status updated successfully"}
