from datetime import datetime

from pydantic import BaseModel


class InspectionBase(BaseModel):
    inspector: str
    product_id: int


class InspectionCreateResponse(InspectionBase):
    pass


class InspectionGetResponse(InspectionBase):
    id: int
    created_at: datetime
    updated_at: datetime


class InspectionUpdateResponse(BaseModel):
    inspector: str
