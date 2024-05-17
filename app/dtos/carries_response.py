from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CarriesBase(BaseModel):
    sender: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[int] = None
    size: Optional[int] = None
    amount: Optional[int] = None


class CarriesCreateResponse(CarriesBase):
    product_id: int


class CarriesGetResponse(CarriesBase):
    id: int
    created_at: datetime
    updated_at: datetime


class CarriesUpdateResponse(CarriesBase):
    pass
