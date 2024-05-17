from __future__ import annotations

from typing import Optional

from tortoise import fields
from tortoise.models import Model

from app.dtos.carries_response import CarriesCreateResponse, CarriesUpdateResponse
from app.models.common import Common
from app.models.products import Product


class Carries(Common, Model):
    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
        "models.Product", related_name="address", on_delete=fields.CASCADE
    )
    product_id: int
    address = fields.CharField(max_length=50)
    sender = fields.CharField(max_length=50)
    contact = fields.IntField()
    size = fields.IntField()
    amount = fields.IntField()

    class Meta:
        table = "carries"

    @classmethod
    async def get_all_by_carries(cls) -> list[Carries]:
        return await cls.all()

    @classmethod
    async def get_by_carries_id(cls, address_id: int) -> Optional[Carries]:
        return await cls.get_or_none(id=address_id)

    @classmethod
    async def create_by_carries(cls, request_data: CarriesCreateResponse) -> Carries:

        return await cls.create(
            product_id=request_data.product_id,
            address=request_data.address,
            sender=request_data.sender,
            contact=request_data.contact,
            size=request_data.size,
            amount=request_data.amount,
        )

    @classmethod
    async def update_by_carries(cls, carries_id: int, request_data: CarriesUpdateResponse) -> Carries:
        carry = await cls.get(id=carries_id)

        # request_data에서 unset(설정되지 않은) 필드를 제외하고, dictionary로 변환
        update_data = request_data.dict(exclude_unset=True)

        # update_data에 있는 각 키와 값을 이용하여, 주소 정보를 업데이트
        for key, value in update_data.items():
            setattr(carry, key, value)  # 객체의 속성을 업데이트

        await carry.save()
        return carry

    @classmethod
    async def delete_by_carries(cls, carries_id: int) -> None:
        carry = await cls.filter(id=carries_id).get()
        await carry.delete()
