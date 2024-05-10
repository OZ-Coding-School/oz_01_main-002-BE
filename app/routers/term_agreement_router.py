from fastapi import APIRouter

from app.dtos.terms_agreement_respones import (
    TermsAgreementResponseIn,
    TermsAgreementResponseOut,
)
from app.services.term_agreement_service import (
    service_create_terms_agreement,
    service_get_all_by_terms_agreement,
)

router = APIRouter(prefix="/api/v1/terms_agreement", tags=["Term_Agreement"], redirect_slashes=False)


@router.get("/", response_model=list[TermsAgreementResponseIn])
async def router_get_by_all_term_agreement() -> list[TermsAgreementResponseIn]:
    return await service_get_all_by_terms_agreement()


@router.post("/", response_model=TermsAgreementResponseOut)
async def router_create_term_agreement(request_data: TermsAgreementResponseOut) -> TermsAgreementResponseOut:
    return await service_create_terms_agreement(request_data)
