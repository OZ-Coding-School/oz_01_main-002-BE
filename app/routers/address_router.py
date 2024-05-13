from fastapi import APIRouter

from app.dtos.address_response import (
    AddressCreateResponse,
    AddressGetResponse,
    AddressUpdateResponse,
)
from app.services.address_service import (
    service_create_address,
    service_delete_address,
    service_get_all_address,
    service_get_by_address_id,
    service_update_address,
)

router = APIRouter(prefix="/api/v1/address", tags=["address"], redirect_slashes=False)


@router.get("/", response_model=list[AddressGetResponse])
async def router_get_all_address() -> list[AddressGetResponse]:
    return await service_get_all_address()


@router.post("/", response_model=AddressCreateResponse)
async def router_create_address(request_data: AddressCreateResponse) -> None:
    return await service_create_address(request_data)


@router.get("/{address_id}", response_model=AddressGetResponse)
async def router_get_dy_address_id(address_id: int) -> AddressGetResponse:
    return await service_get_by_address_id(address_id)


@router.put("/{address_id}", response_model=AddressUpdateResponse)
async def router_update_address(address_id: int, request_data: AddressUpdateResponse) -> AddressUpdateResponse:
    return await service_update_address(address_id, request_data)


@router.delete("/{address_id}")
async def router_delete_address(address_id: int) -> None:
    return await service_delete_address(address_id)
