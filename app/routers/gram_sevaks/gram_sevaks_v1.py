from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config import get_db
from app.models.enums.approval_status import ApprovalStatus, ApprovalStatusRequest
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.services.gramsevak_service import GramsevakService
from app.schemas.gramsevak_schema import (
    GramsevakListItem,
    GramsevakDetailResponse,
    ChangeStatusRequest
)
from app.utils.vx_api_perms_utils import VxAPIPermsUtils


router = APIRouter(
    prefix="/v1/gramsevak",
    tags=["gramsevak"],
    responses={404: {"description": "Not Found"}}
)


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getGramsevakList', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getGramsevakList", response_model=List[GramsevakListItem])
async def get_gramsevak_list(
    searchTerm: Optional[str] = Query(default=None, description="Searching by district name"),
    status: Optional[ApprovalStatusRequest] = Query(default=ApprovalStatusRequest.ALL),
    db: Session = Depends(get_db)
):
    return GramsevakService.get_gramsevak_list(db, search_term=searchTerm, status_filter=status)


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getGramsevakById', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getGramsevakById")
            # response_model=GramsevakDetailResponse)
async def get_gramsevak_by_id(
    id: int = Query(..., alias="id"),
    db: Session = Depends(get_db)
):
    print("In Router for gs")
    return GramsevakService.get_gramsevak_details(db, gramsevak_id=id)


VxAPIPermsUtils.set_perm_patch(path=router.prefix + '/changeStatus', perm=VxAPIPermsEnum.PUBLIC)
@router.patch("/changeStatus")
async def change_gramsevak_status(
    request: ChangeStatusRequest,
    db: Session = Depends(get_db)
):

    return GramsevakService.update_gramsevak_status(
        db, 
        gramsevak_id=request.gramsevak_id,
        new_status=request.status
    )
