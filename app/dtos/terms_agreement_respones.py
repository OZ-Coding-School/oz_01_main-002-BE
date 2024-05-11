from datetime import datetime

from pydantic import BaseModel


class BaseTermsAgreementResponse(BaseModel):
    term_id: int
    user_id: int


class TermsAgreementResponseIn(BaseTermsAgreementResponse):
    id: int
    created_at: datetime
    updated_at: datetime


class TermsAgreementResponseOut(BaseTermsAgreementResponse):
    pass
