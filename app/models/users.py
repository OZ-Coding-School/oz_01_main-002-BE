from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.models.common import Common


class User(Common, Model):
    name = fields.CharField(max_length=30)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=50)
    gender = fields.CharField(max_length=6)
    age = fields.IntField(max_length=3)
    contact = fields.CharField(max_length=15)
    nickname = fields.CharField(max_length=30, unique=True)
    content = fields.TextField(null=True)

    class Meta:
        table = "users"

    @classmethod
    async def get_all_by_user(cls) -> list[User]:
        return await cls.all()

    @classmethod
    async def get_by_user_id(cls, id: str) -> User:
        return await cls.get(id=id)

    @classmethod
    async def create_by_user(
        cls, name: str, email: str, password: str, gender: str, age: int, contact: str, nickname: str, content: str
    ) -> User:
        return await cls.create(
            name=name,
            email=email,
            password=password,
            gender=gender,
            age=age,
            contact=contact,
            nickname=nickname,
            content=content,
        )
