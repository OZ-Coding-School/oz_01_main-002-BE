from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.dtos.terms_agreement_respones import (
    TermsAgreementResponseIn,
    TermsAgreementResponseOut,
)
from app.models.terms import Terms
from app.models.terms_agreements import TermsAgreement
from app.models.users import User


async def service_get_all_by_terms_agreement() -> list[TermsAgreementResponseIn]:
    terms_agreement = await TermsAgreement.get_all_by_terms_agreement()
    return [
        TermsAgreementResponseIn(
            id=terms_agreement.id,
            user_id=terms_agreement.user_id,  # type: ignore
            term_id=terms_agreement.term_id,  # type: ignore
            created_at=terms_agreement.created_at,
            updated_at=terms_agreement.updated_at,
        )
        for terms_agreement in terms_agreement
    ]


async def service_create_terms_agreement(request_data: TermsAgreementResponseOut) -> TermsAgreementResponseOut:
    try:
        await Terms.get_by_terms_id(id=request_data.term_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="term 아이디 값이 없어여")
    try:
        await User.get_by_user_id(id=request_data.user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="user 아이디 값이 없어여")

    terms_agreement = await TermsAgreement.create_by_terms_agreement(request_data)

    return TermsAgreementResponseOut(
        id=terms_agreement.id,
        user_id=terms_agreement.user_id,  # type: ignore
        term_id=terms_agreement.term_id,  # type: ignore
        created_at=terms_agreement.created_at,
        updated_at=terms_agreement.updated_at,
    )
