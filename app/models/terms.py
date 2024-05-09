from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

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
    async def create_by_terms(cls, id: str, name: str, content: str) -> Terms:
        return await cls.create(
            id=id,
            name=name,
            content=content,
            is_required=True,
            is_active=True,
        )
