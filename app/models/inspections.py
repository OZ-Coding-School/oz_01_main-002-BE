from __future__ import annotations

from typing import Optional

from tortoise import fields
from tortoise.models import Model

from app.dtos.inspection_respones import InspectionCreate, InspectionUpdate
from app.models.common import Common
from app.models.products import Product


class Inspection(Common, Model):
    inspector = fields.CharField(max_length=50)
    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
        "models.Product", related_name="inspections", on_delete=fields.CASCADE
    )
    inspection_count = fields.IntField(default=1)

    class Meta:
        table = "inspections"

    @classmethod
    async def get_all_by_inspection(cls) -> list[Inspection]:
        return await cls.all()

    @classmethod
    async def get_by_inspection_detail(cls, product_id: int) -> list[Inspection]:
        return await cls.filter(product_id=product_id)

    @classmethod
    async def get_by_inspection_id(cls, inspection_id: int) -> Inspection:
        return await cls.get(id=inspection_id)

    @classmethod
    async def create_by_inspection(cls, request_data: InspectionCreate) -> Inspection:

        return await cls.create(
            inspector=request_data.inspector,
            product_id=request_data.product_id,
            inspection_count=request_data.inspection_count,
        )

    @classmethod
    async def update_by_inspection(cls, inspection_id: int, request_data: InspectionUpdate) -> None:
        inspection = await cls.get_by_inspection_id(inspection_id)
        if inspection:
            inspection.inspector = request_data.inspector  # 수정할 검수자 지정
            inspection.inspection_count = request_data.inspection_count
            await inspection.save()
