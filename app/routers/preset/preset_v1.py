from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.config import get_db

from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.services.dal.dto.user_hierarchy_dto import DistrictDTO, BlockDTO, GramPanchayatDTO
from app.services.dal.user_hierarchy_dal import GramPanchayatDal, BlockDal, DistrictDal
from app.services.preset_services import PresetService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/preset",
    tags=["preset"],
    responses={404: {"description": "Not Found"}}
)


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getDictricts', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getDictricts"
        # ,response_model=List[DistrictDTO]
            )
async def get_districts(db: Session = Depends(get_db)):
    """Get all active districts"""
    districts = PresetService.get_all_districts(db)
    return districts


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getBlocksByDictrictId', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getBlocksByDictrictId"
    # , response_model=List[BlockDTO]
            )
async def get_blocks_by_district(
    districtId: int = Query(..., alias="districtId"),
    db: Session = Depends(get_db)
):
    """Get blocks by district ID"""
    blocks = PresetService.get_blocks_by_district(db, districtId)
    return blocks


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getGramPanchayatsByBlockId', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getGramPanchayatsByBlockId"
    # , response_model=List[GramPanchayatDTO]
            )
async def get_gram_panchayats_by_block(
    blockId: int = Query(..., alias="blockId"),
    db: Session = Depends(get_db)
):
    """Get gram panchayats by block ID"""
    gps = PresetService.get_gram_panchayats_by_block(db, blockId)
    return gps
