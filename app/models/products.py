from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.models.common import Common


class Product(Common, Model):
    name = fields.CharField(max_length=20)
    content = fields.TextField()
    bid_price = fields.IntField()
    duration = fields.IntField()
    status = fields.CharField(max_length=10)
    modify = fields.BooleanField(default=False)
    grade = fields.CharField(max_length=10)
    category = fields.CharField(max_length=20)
    is_approved = fields.BooleanField(default=False)

    class Meta:
        table = "products"

    @classmethod
    async def get_all_by_products(cls) -> list[Product]:
        return await cls.all()

    @classmethod
    async def create_by_product(
        cls, id: int, name: str, content: str, bid_price: int, duration: int, status: str, grade: str, category: str
    ) -> Product:
        return await cls.create(
            id=id,
            name=name,
            content=content,
            bid_price=bid_price,
            duration=duration,
            status=status,
            grade=grade,
            category=category,
        )

    @classmethod
    async def get_by_product_id(cls, id: int) -> Product:
        return await cls.get(id=id)

    @classmethod
    async def update_by_product_id(
        cls, id: int, name: str, content: str, bid_price: int, duration: int, status: str, grade: str, category: str
    ) -> None:
        await cls.filter(id=id).update(
            name=name,
            content=content,
            bid_price=bid_price,
            duration=duration,
            status=status,
            grade=grade,
            category=category,
        )

    @classmethod
    async def delete_by_product_id(cls, id: int) -> None:
        await cls.filter(id=id).delete()
