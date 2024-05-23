from datetime import datetime
from typing import Optional

import pytz
from pydantic import BaseModel


class AuctionResponse(BaseModel):
    id: Optional[int] = None
    product_id: Optional[int] = None
    status: Optional[bool] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    charge: Optional[int] = None


class AuctionCreate(BaseModel):
    product_id: int
    charge: int


class AuctionUpdate(AuctionResponse):
    status: Optional[bool] = None
