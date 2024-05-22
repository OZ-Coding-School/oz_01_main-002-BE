from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AddressBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    detail_address: Optional[str] = None
    zip_code: Optional[str] = None


class AddressCreateResponse(AddressBase):
    pass


class AddressGetResponse(AddressBase):
    id: int
    is_main: bool
    created_at: datetime
    updated_at: datetime


class AddressUpdateResponse(AddressBase):
    is_main: Optional[bool] = None
