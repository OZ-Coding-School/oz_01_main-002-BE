from datetime import datetime
from typing import Optional

import pytz
from pydantic import BaseModel


class AuctionResponse(BaseModel):
    id: Optional[int] = None
    product_id: Optional[int] = None
    product_name: str
    product_bid_price: int
    product_grade: str
    is_active: Optional[str] = None
    status: Optional[bool] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    charge: Optional[int] = None


class AuctionCreate(BaseModel):
    product_id: int
    charge: int


class AuctionUpdate(BaseModel):
    status: bool
