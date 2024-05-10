from fastapi import APIRouter

from app.dtos.inspection_respones import (
    InspectionCreate,
    InspectionOut,
    InspectionUpdate,
)
from app.services.inspection_service import (
    service_create_inspection,
    service_get_all_inspection,
    service_get_detail_inspection,
    service_get_one_inspection,
    service_update_inspection,
)

router = APIRouter(prefix="/api/v1/inspection", tags=["inspection"], redirect_slashes=False)


@router.get("/", response_model=list[InspectionOut])
async def router_get_all_inspection() -> list[InspectionOut]:
    return await service_get_all_inspection()


@router.post("/", response_model=InspectionCreate)
async def router_create_term(request_data: InspectionCreate) -> InspectionCreate:
    return await service_create_inspection(request_data)


@router.get("/product/{product_id}", response_model=list[InspectionOut])
async def router_get_detail_inspection(product_id: int) -> list[InspectionOut]:
    return await service_get_detail_inspection(product_id)


@router.get("/{inspection_id}", response_model=InspectionOut)
async def router_get_one_inspection(inspection_id: int) -> InspectionOut:
    print(inspection_id)
    return await service_get_one_inspection(inspection_id)


@router.put("/{inspection_id}", response_model=InspectionUpdate)
async def router_update_inspection(inspection_id: int, request_data: InspectionUpdate) -> str:
    return await service_update_inspection(inspection_id, request_data)
