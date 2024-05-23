from fastapi import APIRouter, Depends

from app.dtos.product_response import (
    ProductCreate,
    ProductGetResponse,
    ProductOut,
    ProductUpdate,
)
from app.services.product_service import (
    service_create_product,
    service_delete_product,
    service_get_all_products,
    service_get_by_product_id,
    service_get_products_by_category_id,
    service_get_products_by_user_id,
    service_update_product,
)
from app.services.user_service import get_current_user

router = APIRouter(prefix="/api/v1/products", tags=["product"], redirect_slashes=False)


@router.get("/", response_model=list[ProductGetResponse])
async def router_get_products(_: int = Depends(get_current_user)) -> list[ProductGetResponse]:
    return await service_get_all_products()


@router.post("/", response_model=ProductCreate)
async def router_create_product(
    request_data: ProductCreate, current_user: int = Depends(get_current_user)
) -> ProductCreate:
    return await service_create_product(request_data, current_user)


@router.get("/{product_id}", response_model=ProductOut)
async def router_get_product_id(product_id: int, _: int = Depends(get_current_user)) -> ProductOut:
    return await service_get_by_product_id(product_id)


@router.get("/user/", response_model=list[ProductGetResponse])
async def router_get_products_by_user_id(current_user: int = Depends(get_current_user)) -> list[ProductGetResponse]:
    return await service_get_products_by_user_id(current_user)


@router.get("/categories/{category_id}", response_model=list[ProductOut])
async def router_get_products_by_item_id(category_id: int, _: int = Depends(get_current_user)) -> list[ProductOut]:
    return await service_get_products_by_category_id(category_id)


@router.put("/{product_id}", response_model=ProductUpdate)
async def router_update_product(
    product_id: int, request_data: ProductUpdate, _: int = Depends(get_current_user)
) -> ProductUpdate:
    return await service_update_product(product_id, request_data)


@router.delete("/{product_id}")
async def router_delete_product(product_id: int, _: int = Depends(get_current_user)) -> dict[str, str]:
    await service_delete_product(product_id)
    return {"message": "Product deleted successfully"}
