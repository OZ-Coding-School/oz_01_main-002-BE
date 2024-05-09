from pydantic import BaseModel


class TermsResponse(BaseModel):
    id: str
    name: str
    content: str
    is_required: bool
    is_active: bool
