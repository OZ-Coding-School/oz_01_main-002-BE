from __future__ import annotations

from passlib.context import CryptContext  # type: ignore
from tortoise import fields
from tortoise.models import Model

from app.dtos.user_response import UserSignUpResponse
from app.models.common import Common


class User(Common, Model):
    name = fields.CharField(max_length=30)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)
    gender = fields.CharField(max_length=6)
    age = fields.IntField(max_length=3)
    contact = fields.CharField(max_length=15, unique=True)
    nickname = fields.CharField(max_length=30, unique=True)
    content = fields.TextField(default="나를 표현해주세요")

    class Meta:
        table = "users"

    @classmethod
    async def get_all_by_user(cls) -> list[User]:
        return await cls.all()

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> User:
        return await cls.get(id=user_id)

    @classmethod
    async def create_by_user(cls, request_data: UserSignUpResponse) -> None:

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(request_data.password)

        await cls.create(
            name=request_data.name,
            email=request_data.email,
            password=hashed_password,
            gender=request_data.gender,
            age=request_data.age,
            contact=request_data.contact,
            nickname=request_data.nickname,
        )

    @classmethod
    async def get_by_user_nickname(cls, nickname: str) -> User:
        return await cls.get(nickname=nickname)

    @classmethod
    async def get_by_user_contact(cls, contact: str) -> User:
        return await cls.get(contact=contact)

    @classmethod
    async def verify_user(cls, email: str, password: str) -> bool:
        user = await cls.get_or_none(email=email)

        if user is None:
            return False

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        if pwd_context.verify(password, user.password):
            return True

        return False
