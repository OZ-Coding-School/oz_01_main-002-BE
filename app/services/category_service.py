from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.dtos.category_response import CategoryBaseResponse, CategoryResponse
from app.models.categories import Category


async def service_create_category(request_data: CategoryBaseResponse) -> None:
    try:
        await Category.create_category(request_data)
        raise HTTPException(status_code=201, detail="Created - Category is created")
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Conflict - Category already exists or item_id is not unique",
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
        raise HTTPException(status_code=404, detail="Not Found - Categories not found")


async def service_get_categories_children(parent_id: int) -> list[CategoryResponse]:
    try:
        categories = await Category.get_categories_children(parent_id)
        if len(categories) == 0:
            raise HTTPException(status_code=404, detail="Not Found - Categories not found")
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
        raise HTTPException(status_code=404, detail="Not Found - Categories not found")


async def service_delete_category(item_id: int) -> None:
    try:
        await Category.delete_category(item_id)
        raise HTTPException(status_code=200, detail="OK - Category is deleted")
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Not Found - Categories not found")
