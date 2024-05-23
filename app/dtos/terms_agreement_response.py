from datetime import datetime

from pydantic import BaseModel


class BaseTermsAgreementResponse(BaseModel):
    term_id: int
    user_id: int


class TermsAgreementGetResponse(BaseTermsAgreementResponse):
    id: int
    created_at: datetime
    updated_at: datetime


class TermsAgreementCreateResponse(BaseTermsAgreementResponse):
    pass
