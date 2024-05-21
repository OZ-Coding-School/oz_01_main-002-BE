from datetime import datetime
from typing import List

from pydantic import BaseModel


class ProductBase(BaseModel):
    id: int
    name: str
    bid_price: int


class PaymentBase(BaseModel):
    user_id: int
    total_amount: float


class PaymentCreateResponse(PaymentBase):
    product_ids: List[int]


class PaymentGetResponse(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    products: List[ProductBase]
