from app.dtos.terms_respones import TermsResponse
from app.models.terms import Terms


async def service_get_all_terms() -> list[TermsResponse]:
    terms = await Terms.get_all_by_terms()
    term_list: list[TermsResponse] = []
    for term in terms:
        term_list.append(
            TermsResponse(
                id=term.id, name=term.name, content=term.content, is_required=term.is_required, is_active=term.is_active
            )
        )
    return term_list


async def service_create_term(id: int, name: str, content: str) -> TermsResponse:
    term = await Terms.create_by_terms(id=id, name=name, content=content)
    return TermsResponse(
        id=term.id, name=term.name, content=term.content, is_required=term.is_required, is_active=term.is_active
    )
