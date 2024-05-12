from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.dtos.product_response import ProductCreate, ProductOut, ProductUpdate
from app.models.products import Product
from app.models.users import User


async def service_get_all_products() -> list[ProductOut]:
    try:
        products = await Product.get_all_by_products()
        return [
            ProductOut(
                id=product.id,
                name=product.name,
                content=product.content,
                bid_price=product.bid_price,
                duration=product.duration,
                status=product.status,
                modify=product.modify,
                grade=product.grade,
                category=product.category,
                user_id=product.user_id,
            )
            for product in products
        ]
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="product not found")


async def service_create_product(product_data: ProductCreate) -> ProductCreate:
    try:
        await User.get_by_user_id(id=product_data.user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="user_id not found")

    product = await Product.create_by_product(product_data)
    return ProductCreate(
        name=product.name,
        content=product.content,
        bid_price=product.bid_price,
        duration=product.duration,
        user_id=product.user_id,
        status=product.status,
        modify=product.modify,
        grade=product.grade,
        category=product.category,
    )


async def service_get_by_product_id(id: int) -> ProductOut:
    product = await Product.get_by_product_id(id)
    if product:
        return ProductOut(
            id=product.id,
            name=product.name,
            content=product.content,
            bid_price=product.bid_price,
            duration=product.duration,
            status=product.status,
            modify=product.modify,
            grade=product.grade,
            category=product.category,
            user_id=product.user_id,
        )
    raise HTTPException(status_code=404, detail="Product not found")


async def service_update_product(id: int, product_data: ProductUpdate) -> ProductUpdate:
    try:
        product = await Product.get_by_product_id(id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="not found")

    await Product.update_by_product_id(id, product_data)

    new_product = await Product.get_by_product_id(id)

    return ProductUpdate(
        name=new_product.name,
        content=new_product.content,
        bid_price=new_product.bid_price,
        duration=new_product.duration,
        status=new_product.status,
        modify=product.modify,
        grade=new_product.grade,
        category=new_product.category,
    )


async def service_delete_product(id: int) -> None:
    try:
        product = await Product.get_by_product_id(id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="not found")

    await product.delete()
