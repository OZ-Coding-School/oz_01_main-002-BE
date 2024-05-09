from fastapi import HTTPException

from app.dtos.product_response import ProductResponse
from app.models.products import Product


async def service_get_all_products() -> list[ProductResponse]:
    products = await Product.get_all_by_products()
    product_list: list[ProductResponse] = []
    for product in products:
        product_list.append(
            ProductResponse(
                id=product.id,
                name=product.name,
                content=product.content,
                bid_price=product.bid_price,
                duration=product.duration,
                status=product.status,
                modify=product.modify,
                grade=product.grade,
                category=product.category,
            )
        )
    return product_list


async def service_create_product(
    id: int, name: str, content: str, bid_price: int, duration: int, status: str, grade: str, category: str
) -> ProductResponse:
    product = await Product.create_by_product(
        id=id,
        name=name,
        content=content,
        bid_price=bid_price,
        duration=duration,
        status=status,
        grade=grade,
        category=category,
    )
    return ProductResponse(
        id=product.id,
        name=product.name,
        content=product.content,
        bid_price=product.bid_price,
        duration=product.duration,
        status=product.status,
        modify=product.modify,
        grade=product.grade,
        category=product.category,
    )
