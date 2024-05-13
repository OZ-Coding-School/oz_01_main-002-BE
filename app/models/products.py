from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.dtos.product_response import ProductCreate, ProductUpdate
from app.models.common import Common
from app.models.users import User


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
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="products", on_delete=fields.CASCADE
    )
    user_id: int

    class Meta:
        table = "products"

    @classmethod
    async def get_all_by_products(cls) -> list[Product]:
        return await cls.all()

    @classmethod
    async def create_by_product(cls, product_data: ProductCreate) -> Product:
        return await cls.create(
            user_id=product_data.user_id,
            name=product_data.name,
            content=product_data.content,
            bid_price=product_data.bid_price,
            duration=product_data.duration,
            status=product_data.status,
            modify=product_data.modify,
            grade=product_data.grade,
            category=product_data.category,
        )

    @classmethod
    async def get_by_product_id(cls, id: int) -> Product:
        return await cls.get(id=id)

    @classmethod
    async def update_by_product_id(cls, id: int, product_data: ProductUpdate) -> None:
        await cls.filter(id=id).update(
            name=product_data.name,
            content=product_data.content,
            bid_price=product_data.bid_price,
            duration=product_data.duration,
            status=product_data.status,
        )

    @classmethod
    async def delete_by_product_id(cls, id: int) -> None:
        await cls.filter(id=id).delete()
