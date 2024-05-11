from fastapi import APIRouter

from app.dtos.terms_respones import TermsResponseIn, TermsResponseOut
from app.services.term_service import service_create_term, service_get_all_by_terms

router = APIRouter(prefix="/api/v1/terms", tags=["Term"], redirect_slashes=False)


@router.get("/", response_model=list[TermsResponseIn])
async def router_get_by_all_term() -> list[TermsResponseIn]:
    return await service_get_all_by_terms()


@router.post("/", response_model=TermsResponseOut)
async def router_create_term(request_data: TermsResponseOut) -> TermsResponseOut:
    return await service_create_term(request_data)
