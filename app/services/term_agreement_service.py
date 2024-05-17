from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.dtos.terms_agreement_response import (
    TermsAgreementCreateResponse,
    TermsAgreementGetResponse,
)
from app.models.terms import Terms
from app.models.terms_agreements import TermsAgreement
from app.models.users import User


async def service_get_all_by_terms_agreement() -> list[TermsAgreementGetResponse]:
    terms_agreement = await TermsAgreement.get_all_by_terms_agreement()
    return [
        TermsAgreementGetResponse(
            id=terms_agreement.id,
            user_id=terms_agreement.user_id,
            term_id=terms_agreement.term_id,
            created_at=terms_agreement.created_at,
            updated_at=terms_agreement.updated_at,
        )
        for terms_agreement in terms_agreement
    ]


async def service_create_terms_agreement(request_data: TermsAgreementCreateResponse) -> None:
    try:
        await Terms.get_by_terms_id(id=request_data.term_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="term 아이디 값이 없어여")
    try:
        await User.get_by_user_id(user_id=request_data.user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="user 아이디 값이 없어여")

    terms_agreement = await TermsAgreement.create_by_terms_agreement(request_data)

    if terms_agreement:
        raise HTTPException(status_code=201, detail="terms_agreement 성공적으로 생성되었습니다.")
