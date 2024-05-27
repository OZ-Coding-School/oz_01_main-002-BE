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
    category: str
    final_price: int
    is_active: Optional[str] = None
    status: Optional[bool] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    charge: Optional[float] = None
    product_content: str
    user_nickname: str
    user_content: str


class AuctionCreate(BaseModel):
    product_id: int
    charge: float
    final_price: int


class AuctionUpdate(BaseModel):
    status: bool
