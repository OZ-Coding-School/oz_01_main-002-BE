from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.dtos.terms_agreement_response import TermsAgreementCreateResponse
from app.models.common import Common
from app.models.terms import Terms
from app.models.users import User


class TermsAgreement(Common, Model):

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="terms_agreements", on_delete=fields.CASCADE
    )
    user_id: int
    term: fields.ForeignKeyRelation[Terms] = fields.ForeignKeyField(
        "models.Terms", related_name="terms_agreements", on_delete=fields.CASCADE
    )
    term_id: int

    class Meta:
        table = "terms_agreements"

    @classmethod
    async def get_all_by_terms_agreement(cls) -> list[TermsAgreement]:
        return await cls.all()

    @classmethod
    async def create_by_terms_agreement(cls, request_data: TermsAgreementCreateResponse) -> TermsAgreement:
        return await cls.create(
            user_id=request_data.user_id,
            term_id=request_data.term_id,
        )
