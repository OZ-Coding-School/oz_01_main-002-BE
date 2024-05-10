from datetime import datetime

from pydantic import BaseModel


class BaseTermResponse(BaseModel):
    name: str
    content: str


class TermsResponseIn(BaseTermResponse):
    id: int
    is_required: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TermsResponseOut(BaseTermResponse):
    pass
