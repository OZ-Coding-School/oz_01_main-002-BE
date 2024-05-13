from fastapi import APIRouter

from app.dtos.terms_response import TermsResponseCreate, TermsResponseGet
from app.services.term_service import service_create_term, service_get_all_by_terms

router = APIRouter(prefix="/api/v1/terms", tags=["Term"], redirect_slashes=False)


@router.get("/", response_model=list[TermsResponseGet])
async def router_get_by_all_term() -> list[TermsResponseGet]:
    return await service_get_all_by_terms()


@router.post("/", response_model=TermsResponseCreate)
async def router_create_term(request_data: TermsResponseCreate) -> TermsResponseCreate:
    return await service_create_term(request_data)
