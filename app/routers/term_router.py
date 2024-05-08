from fastapi import APIRouter, Request

from app.dtos.terms_respones import TermsResponse
from app.models.terms import Terms
from app.services.term_service import service_create_term, service_get_all_terms

router = APIRouter(prefix="/api/v1/terms", tags=["Term"], redirect_slashes=False)


@router.get("/", response_model=list[TermsResponse])
async def router_get_article_and_comments() -> list[TermsResponse]:
    return await service_get_all_terms()


@router.post("/", response_model=TermsResponse)
async def router_create_term(request_data: TermsResponse) -> TermsResponse:
    name = request_data.name
    content = request_data.content
    id = request_data.id
    return await service_create_term(id=id, name=name, content=content)
