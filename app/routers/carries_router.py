from fastapi import APIRouter, Depends

from app.dtos.carries_response import (
    CarriesCreateResponse,
    CarriesGetResponse,
    CarriesUpdateResponse,
)
from app.services.carries_service import (
    service_create_carries,
    service_delete_carries,
    service_get_all_carries,
    service_get_by_carries_id,
    service_update_carries,
)
from app.services.user_service import get_current_user

router = APIRouter(prefix="/api/v1/carries", tags=["carries"], redirect_slashes=False)


@router.get("/", response_model=list[CarriesGetResponse])
async def router_get_all_carries(_: int = Depends(get_current_user)) -> list[CarriesGetResponse]:
    return await service_get_all_carries()


@router.post("/", response_model=CarriesCreateResponse)
async def router_create_carries(request_data: CarriesCreateResponse, _: int = Depends(get_current_user)) -> None:
    return await service_create_carries(request_data)


@router.get("/{carries_id}", response_model=CarriesGetResponse)
async def router_get_dy_carries_id(carries_id: int, _: int = Depends(get_current_user)) -> CarriesGetResponse:
    return await service_get_by_carries_id(carries_id)


@router.put("/{carries_id}", response_model=CarriesUpdateResponse)
async def router_update_carries(
    carries_id: int, request_data: CarriesUpdateResponse, _: int = Depends(get_current_user)
) -> CarriesUpdateResponse:
    return await service_update_carries(carries_id, request_data)


@router.delete("/{carries_id}")
async def router_delete_carries(carries_id: int, _: int = Depends(get_current_user)) -> None:
    return await service_delete_carries(carries_id)
