from fastapi import APIRouter

from app.dtos.product_response import ProductResponse
from app.services.product_service import (
    service_create_product,
    service_delete_product,
    service_get_all_products,
    service_get_by_product_id,
    service_update_product,
)

router = APIRouter(prefix="/api/v1/products", tags=["product"], redirect_slashes=False)


@router.get("/", response_model=list[ProductResponse])
async def router_get_products() -> list[ProductResponse]:
    return await service_get_all_products()


@router.post("/", response_model=ProductResponse)
async def router_create_product(request_data: ProductResponse) -> ProductResponse:
    id = request_data.id
    name = request_data.name
    content = request_data.content
    bid_price = request_data.bid_price
    duration = request_data.duration
    status = request_data.status
    grade = request_data.grade
    category = request_data.category
    return await service_create_product(
        id=id,
        name=name,
        content=content,
        bid_price=bid_price,
        duration=duration,
        status=status,
        grade=grade,
        category=category,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def router_get_product_id(product_id: int) -> list[ProductResponse]:
    return await service_get_by_product_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def router_update_product(product_id: int, request_data: ProductResponse) -> ProductResponse:
    product_id = request_data.id
    name = request_data.name
    content = request_data.content
    bid_price = request_data.bid_price
    duration = request_data.duration
    status = request_data.status
    grade = request_data.grade
    category = request_data.category
    return await service_update_product(
        product_id=product_id,
        name=name,
        content=content,
        bid_price=bid_price,
        duration=duration,
        status=status,
        grade=grade,
        category=category,
    )


@router.delete("/{product_id}")
async def router_delete_product(product_id: int) -> dict[str, str]:
    await service_delete_product(product_id)
    return {"message": "Product deleted successfully"}
