from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.dtos.product_response import (
    ProductCreate,
    ProductGetResponse,
    ProductOut,
    ProductUpdate,
)
from app.models.categories import Category
from app.models.products import Product
from app.models.users import User


async def service_get_all_products() -> list[ProductGetResponse]:
    try:
        products = await Product.get_all_by_products()
        products_out = []
        for product in products:
            category = await Category.get(id=product.category_id)

            product_out = ProductGetResponse(
                name=product.name,
                content=product.content,
                bid_price=product.bid_price,
                duration=product.duration,
                status=product.status,
                modify=product.modify,
                grade=product.grade,
                category=category.name,
                is_approved=product.is_approved,
            )
            products_out.append(product_out)
        return products_out
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="product not found")


async def service_create_product(product_data: ProductCreate, current_user: int) -> ProductCreate:
    try:
        await User.get_by_user_id(user_id=current_user)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="user_id not found")

    product = await Product.create_by_product(product_data, current_user)
    return ProductCreate(
        name=product.name,
        content=product.content,
        bid_price=product.bid_price,
        duration=product.duration,
        user_id=current_user,
        status=product.status,
        modify=product.modify,
        grade=product.grade,
        category_id=product.category_id,
    )


async def service_get_by_product_id(product_id: int) -> ProductOut:
    product = await Product.get_by_product_id(product_id)
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
            category_id=product.category_id,
            user_id=product.user_id,
        )
    raise HTTPException(status_code=404, detail="Product not found")


async def service_get_products_by_user_id(current_user: int) -> list[ProductGetResponse]:
    try:
        await User.get_by_user_id(user_id=current_user)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    products = await Product.get_by_user_id(current_user)
    products_response = []
    for product in products:
        category = await Category.get(id=product.category_id)
        product_response = ProductGetResponse(
            name=product.name,
            content=product.content,
            bid_price=product.bid_price,
            duration=product.duration,
            status=product.status,
            modify=product.modify,
            grade=product.grade,
            category=category.name,
            is_approved=product.is_approved,
        )
        products_response.append(product_response)
    return products_response


async def service_get_products_by_category_id(category_id: int) -> list[ProductOut]:
    try:
        await Category.get(id=category_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="category not found")

    products = await Product.get_by_category_id(category_id)
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
            category_id=product.category_id,
            user_id=product.user_id,
        )
        for product in products
    ]


async def service_update_product(product_id: int, product_data: ProductUpdate) -> ProductUpdate:
    try:
        product = await Product.get_by_product_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="not found")

    new_product = await Product.update_by_product_id(product_id, product_data)

    return ProductUpdate(
        name=new_product.name,
        content=new_product.content,
        bid_price=new_product.bid_price,
        duration=new_product.duration,
        status=new_product.status,
    )


async def service_delete_product(product_id: int) -> None:
    try:
        product = await Product.get_by_product_id(product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="not found")

    await product.delete()
