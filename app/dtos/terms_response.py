from datetime import datetime

from pydantic import BaseModel


class BaseTermResponse(BaseModel):
    name: str
    content: str


class TermsResponseGet(BaseTermResponse):
    id: int
    is_required: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TermsResponseCreate(BaseTermResponse):
    pass


class TermIDResponse(BaseModel):
    id: int
