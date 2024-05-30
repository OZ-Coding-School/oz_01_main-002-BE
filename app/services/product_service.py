from fastapi import HTTPException, UploadFile
from tortoise.exceptions import DoesNotExist

from app.dtos.image_response import ImageClassificationResponse
from app.dtos.product_response import ProductCreate, ProductGetResponse, ProductUpdate
from app.models.categories import Category
from app.models.products import Product
from app.models.users import User
from app.models.winners import Winner
from app.services.image_service import service_get_images, service_save_image


async def service_get_all_products() -> list[ProductGetResponse]:
    try:
        products = await Product.get_all_by_products()
        products_out = []
        for product in products:
            category = await Category.get(id=product.category_id)
            winner = await Winner.get_by_winner(product.id)
            if winner:
                user = await User.get(id=winner.user_id)
                winner_details = {
                    "winner_user_id": winner.user_id,
                    "winner_nickname": user.nickname,
                    "winner_bid_price": winner.bid_price,
                }
            else:
                winner_details = {
                    "winner_user_id": None,
                    "winner_nickname": None,
                    "winner_bid_price": None,
                }
            product_out = ProductGetResponse(
                id=product.id,
                name=product.name,
                content=product.content,
                bid_price=product.bid_price,
                duration=product.duration,
                status=product.status,
                modify=product.modify,
                grade=product.grade,
                category=category.name,
                is_approved=product.is_approved,
                **winner_details
            )
            products_out.append(product_out)
        return products_out
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="product not found")


async def service_create_product(product_data: ProductCreate, current_user: int, file1: UploadFile, file2: UploadFile, file3: UploadFile) -> ProductCreate:
    try:
        await User.get_by_user_id(user_id=current_user)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="user_id not found")

    product = await Product.create_by_product(product_data, current_user)

    product_image = ImageClassificationResponse(component="product", target_id=product.id)

    await service_save_image(file1, file2, file3, product_image)

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


async def service_get_by_product_id(product_id: int) -> ProductGetResponse:
    try:
        product = await Product.get_by_product_id(product_id)
        HTTPException(status_code=404, detail="product not found")
        category = await Category.get(id=product.category_id)
        winner = await Winner.get_by_winner(product.id)
        images = await service_get_images("product", product.id)
        if images is None:
            raise HTTPException(status_code=404, detail="image not found")
        image_urls = [img.url for img in images]
        if winner:
            user = await User.get(id=winner.user_id)
            winner_details = {
                "winner_user_id": winner.user_id,
                "winner_nickname": user.nickname,
                "winner_bid_price": winner.bid_price,
            }
        else:
            winner_details = {
                "winner_user_id": None,
                "winner_nickname": None,
                "winner_bid_price": None,
            }
        return ProductGetResponse(
            id=product.id,
            name=product.name,
            content=product.content,
            bid_price=product.bid_price,
            duration=product.duration,
            status=product.status,
            modify=product.modify,
            grade=product.grade,
            category=category.name,
            is_approved=product.is_approved,
            images=image_urls,
            **winner_details
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="product not found")


async def service_get_products_by_user_id(current_user: int) -> list[ProductGetResponse]:
    try:
        await User.get_by_user_id(user_id=current_user)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    products = await Product.get_by_user_id(current_user)
    products_response = []
    for product in products:
        category = await Category.get(id=product.category_id)
        winner = await Winner.get_by_winner(product.id)
        images = await service_get_images("product", product.id)
        if images is None:
            raise HTTPException(status_code=404, detail="image not found")
        image_urls = [img.url for img in images]
        if winner:
            user = await User.get(id=winner.user_id)
            winner_details = {
                "winner_user_id": winner.user_id,
                "winner_nickname": user.nickname,
                "winner_bid_price": winner.bid_price,
            }
        else:
            winner_details = {
                "winner_user_id": None,
                "winner_nickname": None,
                "winner_bid_price": None,
            }
        product_response = ProductGetResponse(
            id=product.id,
            name=product.name,
            content=product.content,
            bid_price=product.bid_price,
            duration=product.duration,
            status=product.status,
            modify=product.modify,
            grade=product.grade,
            category=category.name,
            is_approved=product.is_approved,
            images=image_urls,
            **winner_details
        )
        products_response.append(product_response)
    return products_response


async def service_get_products_by_category_id(category_id: int) -> list[ProductGetResponse]:
    products = await Product.get_by_category_id(category_id)
    products_out = []
    for product in products:
        category = await Category.get(id=category_id)
        if not category:
            raise HTTPException(status_code=404, detail="category not found")
        winner = await Winner.get_by_winner(product.id)
        images = await service_get_images("product", product.id)
        if images is None:
            raise HTTPException(status_code=404, detail="image not found")
        image_urls = [img.url for img in images]
        if winner:
            user = await User.get(id=winner.user_id)
            winner_details = {
                "winner_user_id": winner.user_id,
                "winner_nickname": user.nickname,
                "winner_bid_price": winner.bid_price,
            }
        else:
            winner_details = {
                "winner_user_id": None,
                "winner_nickname": None,
                "winner_bid_price": None,
            }
        product_out = ProductGetResponse(
            id=product.id,
            name=product.name,
            content=product.content,
            bid_price=product.bid_price,
            duration=product.duration,
            status=product.status,
            modify=product.modify,
            grade=product.grade,
            category=category.name,
            is_approved=product.is_approved,
            images=image_urls,
            **winner_details
        )
        products_out.append(product_out)
    return products_out


async def service_update_product(product_id: int, product_data: ProductUpdate) -> ProductUpdate:
    try:
        await Product.get_by_product_id(product_id)
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
