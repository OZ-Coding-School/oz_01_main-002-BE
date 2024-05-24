from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.dtos.product_response import ProductCreate, ProductUpdate
from app.models.categories import Category
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
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        "models.Category", related_name="categories", on_delete=fields.CASCADE
    )
    is_approved = fields.BooleanField(default=False)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="products", on_delete=fields.CASCADE
    )
    user_id: int
    category_id: int
    category_name: str

    class Meta:
        table = "products"

    @classmethod
    async def get_all_by_products(cls) -> list[Product]:
        products = await cls.all()
        for product in products:
            category = await product.category
            product.category_name = category.name
        return products

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
            category_id=product_data.category_id,
        )

    @classmethod
    async def get_by_product_id(cls, product_id: int) -> Product:
        product = await cls.get(id=product_id).prefetch_related("category")
        category = await product.category
        product.category_name = category.name
        return product

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> list[Product]:
        products = await cls.filter(user_id=user_id).all()
        for product in products:
            category = await product.category
            product.category_name = category.name
        return products

    @classmethod
    async def get_by_category_id(cls, category_id: int) -> list[Product]:
        products = await cls.filter(category_id=category_id).all()
        for product in products:
            category = await product.category
            product.category_name = category.name
        return products

    @classmethod
    async def update_by_product_id(cls, product_id: int, request_data: ProductUpdate) -> Product:
        product = await cls.get(id=product_id)

        update_data = request_data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        await product.save()
        return product

    @classmethod
    async def delete_by_product_id(cls, product_id: int) -> None:
        await cls.filter(id=product_id).delete()
