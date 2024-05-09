from fastapi import APIRouter

from app.dtos.product_response import ProductResponse
from app.services.product_service import (
    service_create_product,
    service_get_all_products,
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
