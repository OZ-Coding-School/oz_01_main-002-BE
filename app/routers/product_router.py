from fastapi import APIRouter

from app.dtos.product_response import ProductCreate, ProductOut, ProductUpdate
from app.services.product_service import (
    service_create_product,
    service_delete_product,
    service_get_all_products,
    service_get_by_product_id,
    service_get_products_by_user_id,
    service_update_product,
)

router = APIRouter(prefix="/api/v1/products", tags=["product"], redirect_slashes=False)


@router.get("/", response_model=list[ProductOut])
async def router_get_products() -> list[ProductOut]:
    return await service_get_all_products()


@router.post("/", response_model=ProductCreate)
async def router_create_product(request_data: ProductCreate) -> ProductCreate:
    return await service_create_product(request_data)


@router.get("/{product_id}", response_model=ProductOut)
async def router_get_product_id(product_id: int) -> ProductOut:
    return await service_get_by_product_id(product_id)


@router.get("/user/{user_id}", response_model=list[ProductOut])
async def router_get_products_by_user_id(user_id: int) -> list[ProductOut]:
    return await service_get_products_by_user_id(user_id)


@router.put("/{product_id}", response_model=ProductUpdate)
async def router_update_product(product_id: int, request_data: ProductUpdate) -> ProductUpdate:
    return await service_update_product(product_id, request_data)


@router.delete("/{product_id}")
async def router_delete_product(product_id: int) -> dict[str, str]:
    await service_delete_product(product_id)
    return {"message": "Product deleted successfully"}
