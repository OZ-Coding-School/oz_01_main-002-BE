from app.dtos.terms_response import TermsResponseCreate, TermsResponseGet
from app.models.terms import Terms


async def service_get_all_by_terms() -> list[TermsResponseGet]:
    terms = await Terms.get_all_by_terms()
    return [
        TermsResponseGet(
            id=term.id,
            name=term.name,
            content=term.content,
            is_required=term.is_required,
            is_active=term.is_active,
            created_at=term.created_at,
            updated_at=term.updated_at,
        )
        for term in terms
    ]


async def service_create_term(request_data: TermsResponseCreate) -> TermsResponseCreate:
    term = await Terms.create_by_terms(request_data)
    return TermsResponseCreate(
        name=term.name,
        content=term.content,
    )
