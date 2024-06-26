from __future__ import annotations

from passlib.context import CryptContext  # type: ignore
from tortoise import fields
from tortoise.models import Model

from app.dtos.user_response import (
    UserCoinCreateResponse,
    UserSignUpResponse,
    UserUpdateProfileResponse,
)
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
    coin = fields.FloatField(default=0.0)

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

    @classmethod
    async def update_by_user_coin(cls, request_data: UserCoinCreateResponse, current_user: int) -> None:
        user = await cls.get_by_user_id(current_user)
        user.coin = request_data.coin
        await user.save()

    @classmethod
    async def update_by_user(cls, request_data: UserUpdateProfileResponse, current_user: int) -> User:
        user = await cls.get_by_user_id(current_user)

        # request_data에서 unset(설정되지 않은) 필드를 제외하고, dictionary로 변환
        update_data = request_data.dict(exclude_unset=True)

        # update_data에 있는 각 키와 값을 이용하여, 주소 정보를 업데이트
        for key, value in update_data.items():
            setattr(user, key, value)  # 객체의 속성을 업데이트

        await user.save()
        return user
