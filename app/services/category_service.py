from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.dtos.category_response import CategoryBaseResponse, CategoryResponse
from app.models.categories import Category


async def service_create_category(request_data: CategoryBaseResponse) -> CategoryBaseResponse:
    try:
        category = await Category.create_category(request_data)
        return CategoryResponse(
            id=category.id, item_id=category.item_id, parent_id=category.parent_id, sqe=category.sqe, name=category.name
        )
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Category already exists or item_id is not unique",
        )


async def service_get_all_categories() -> list[CategoryResponse]:
    categories = await Category.get_all_by_categories()
    return [
        CategoryResponse(
            id=category.id, item_id=category.item_id, parent_id=category.parent_id, sqe=category.sqe, name=category.name
        )
        for category in categories
    ]


async def service_get_category_by_item_id(item_id: int) -> CategoryResponse:
    try:
        category = await Category.get_by_category_item_id(item_id)
        return CategoryResponse(
            id=category.id, item_id=category.item_id, parent_id=category.parent_id, sqe=category.sqe, name=category.name
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")


async def service_get_categories_children(parent_id: int) -> list[CategoryResponse]:
    try:
        categories = await Category.get_categories_children(parent_id)
        return [
            CategoryResponse(
                id=category.id,
                item_id=category.item_id,
                parent_id=category.parent_id,
                sqe=category.sqe,
                name=category.name,
            )
            for category in categories
        ]
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Categories not found")


async def service_delete_category(item_id: int) -> None:
    try:
        await Category.delete_category(item_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")
