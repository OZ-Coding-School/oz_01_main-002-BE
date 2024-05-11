from fastapi import APIRouter

from app.dtos.category_response import CategoryBaseResponse, CategoryResponse
from app.services.category_service import (
    service_create_category,
    service_delete_category,
    service_get_all_categories,
    service_get_categories_children,
    service_get_category_by_item_id,
)

router = APIRouter(prefix="/categories", tags=["Categories"], redirect_slashes=False)


@router.post("/", response_model=CategoryBaseResponse)
async def router_create_category(request_data: CategoryBaseResponse) -> CategoryBaseResponse:
    return await service_create_category(request_data=request_data)


@router.get("/", response_model=list[CategoryResponse])
async def router_get_all_categories() -> list[CategoryResponse]:
    return await service_get_all_categories()


@router.get("/{category_id}", response_model=CategoryResponse)
async def router_get_category_id(item_id: int) -> CategoryResponse:
    return await service_get_category_by_item_id(item_id)


@router.get("/parent_id/{parent_id}", response_model=list[CategoryResponse])
async def router_parent_id(parent_id: int) -> list[CategoryResponse]:
    return await service_get_categories_children(parent_id)


@router.delete("/{category_id}")
async def router_delete_category(category_id: int) -> None:
    return await service_delete_category(category_id)
