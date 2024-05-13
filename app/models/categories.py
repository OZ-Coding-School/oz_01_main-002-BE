from __future__ import annotations

from typing import Optional

from tortoise import fields
from tortoise.models import Model

from app.dtos.category_response import CategoryBaseResponse


class Category(Model):
    id = fields.IntField(pk=True)
    item_id = fields.IntField(unique=True)
    parent_id = fields.IntField()
    sqe = fields.IntField()
    name = fields.CharField(max_length=50)

    class Meta:
        table = "categories"

    @classmethod
    async def get_all_by_categories(cls) -> list[Category]:
        return await cls.all()

    @classmethod
    async def get_by_category_item_id(cls, item_id: int) -> Category:
        return await cls.filter(item_id=item_id).get()

    @classmethod
    async def create_category(cls, request_data: CategoryBaseResponse) -> Category:
        return await cls.create(
            item_id=request_data.item_id,
            parent_id=request_data.parent_id,
            sqe=request_data.sqe,
            name=request_data.name,
        )

    @classmethod
    async def delete_category(cls, item_id: int) -> None:
        await cls.filter(item_id=item_id).delete()

    @classmethod
    async def get_categories_children(cls, parent_id: int) -> list[Category]:
        return await cls.filter(parent_id=parent_id).order_by("sqe").all()
