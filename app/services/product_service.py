from fastapi import HTTPException

from app.dtos.product_response import ProductResponse
from app.models.products import Product


async def service_get_all_products() -> list[ProductResponse]:
    products = await Product.get_all_by_products()
    return [
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
        for product in products
    ]


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


async def service_get_by_product_id(product_id: int) -> list[ProductResponse]:
    product = await Product.get_by_product_id(product_id)
    if product:
        return [
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
        ]
    raise HTTPException(status_code=404, detail="Product not found")


async def service_update_product(
    product_id: int, name: str, content: str, bid_price: int, duration: int, status: str, grade: str, category: str
) -> ProductResponse:
    try:
        product = await Product.get_by_product_id(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="not found")

    await Product.update_by_product_id(
        id=product.id,
        name=name,
        content=content,
        bid_price=bid_price,
        duration=duration,
        status=status,
        grade=grade,
        category=category,
    )

    new_product = await Product.get_by_product_id(product_id)

    return ProductResponse(
        id=new_product.id,
        name=new_product.name,
        content=new_product.content,
        bid_price=new_product.bid_price,
        duration=new_product.duration,
        status=new_product.status,
        modify=product.modify,
        grade=new_product.grade,
        category=new_product.category,
    )


async def service_delete_product(product_id: int) -> None:
    try:
        product = await Product.get_by_product_id(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="not found")

    await product.delete()
