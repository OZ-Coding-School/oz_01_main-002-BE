from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.dtos.terms_respones import TermsResponseOut
from app.models.common import Common


class Terms(Common, Model):
    name = fields.CharField(max_length=255)
    content = fields.TextField()
    is_required = fields.BooleanField(default=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "terms"

    @classmethod
    async def get_all_by_terms(cls) -> list[Terms]:
        return await cls.all()

    @classmethod
    async def get_by_terms_id(cls, id: int) -> Terms:
        return await cls.get(id=id)

    @classmethod
    async def create_by_terms(cls, request_data: TermsResponseOut) -> Terms:
        return await cls.create(
            name=request_data.name,
            content=request_data.content,
        )
