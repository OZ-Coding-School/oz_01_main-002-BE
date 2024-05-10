from datetime import datetime

from pydantic import BaseModel


class InspectionBase(BaseModel):
    inspector: str
    product_id: int
    inspection_count: int


class InspectionCreate(InspectionBase):
    pass


class InspectionOut(InspectionBase):
    id: int
    created_at: datetime
    updated_at: datetime


class InspectionUpdate(BaseModel):
    inspector: str
    inspection_count: int
