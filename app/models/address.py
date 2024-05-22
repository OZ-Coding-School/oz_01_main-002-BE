from __future__ import annotations

from typing import Optional

from tortoise import fields
from tortoise.models import Model

from app.dtos.address_response import AddressCreateResponse, AddressUpdateResponse
from app.models.common import Common
from app.models.users import User


class Address(Common, Model):
    name = fields.CharField(max_length=50)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="address", on_delete=fields.CASCADE
    )
    address = fields.CharField(max_length=50)
    detail_address = fields.CharField(max_length=50)
    zip_code = fields.CharField(max_length=50)
    is_main = fields.BooleanField(default=True)
    user_id: int

    class Meta:
        table = "address"

    @classmethod
    async def get_all_by_address(cls) -> list[Address]:
        return await cls.all()

    @classmethod
    async def get_by_address_id(cls, address_id: int) -> Optional[Address]:
        return await cls.get_or_none(id=address_id)

    @classmethod
    async def create_by_address(cls, request_data: AddressCreateResponse, current_user: int) -> Address:

        return await cls.create(
            name=request_data.name,
            address=request_data.address,
            detail_address=request_data.detail_address,
            zip_code=request_data.zip_code,
            user_id=current_user,
        )

    @classmethod
    async def update_by_address(cls, address_id: int, request_data: AddressUpdateResponse) -> Address:
        address = await cls.get(id=address_id)

        # request_data에서 unset(설정되지 않은) 필드를 제외하고, dictionary로 변환
        update_data = request_data.dict(exclude_unset=True)

        # update_data에 있는 각 키와 값을 이용하여, 주소 정보를 업데이트
        for key, value in update_data.items():
            setattr(address, key, value)  # 객체의 속성을 업데이트

        await address.save()
        return address

    @classmethod
    async def delete_by_address(cls, address_id: int) -> None:
        address = await cls.filter(id=address_id).get()
        await address.delete()
