from fastapi import APIRouter, Depends

from app.dtos.terms_agreement_response import (
    TermsAgreementCreateResponse,
    TermsAgreementGetResponse,
)
from app.services.term_agreement_service import (
    service_create_terms_agreement,
    service_get_all_by_terms_agreement,
)
from app.services.user_service import get_current_user

router = APIRouter(prefix="/api/v1/terms_agreement", tags=["Term_Agreement"], redirect_slashes=False)


@router.get("/", response_model=list[TermsAgreementGetResponse])
async def router_get_by_all_term_agreement(_: int = Depends(get_current_user)) -> list[TermsAgreementGetResponse]:
    return await service_get_all_by_terms_agreement()


@router.post("/", response_model=TermsAgreementCreateResponse)
async def router_create_term_agreement(
    request_data: TermsAgreementCreateResponse, current_user: int = Depends(get_current_user)
) -> None:
    return await service_create_terms_agreement(request_data, current_user)
