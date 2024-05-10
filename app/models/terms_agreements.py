from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.dtos.terms_agreement_respones import TermsAgreementResponseOut
from app.models.common import Common
from app.models.terms import Terms
from app.models.users import User


class TermsAgreement(Common, Model):

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="terms_agreements", on_delete=fields.CASCADE
    )
    term: fields.ForeignKeyRelation[Terms] = fields.ForeignKeyField(
        "models.Terms", related_name="terms_agreements", on_delete=fields.CASCADE
    )

    class Meta:
        table = "terms_agreements"

    @classmethod
    async def get_all_by_terms_agreement(cls) -> list[Terms_Agreement]:
        return await cls.all()

    @classmethod
    async def create_by_terms_agreement(cls, request_data: TermsAgreementResponseOut) -> Terms_Agreement:
        return await cls.create(
            user_id=request_data.user_id,
            term_id=request_data.term_id,
        )
