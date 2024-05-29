from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    content: str
    bid_price: int
    duration: int
    status: str
    modify: bool
    grade: str
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    bid_price: Optional[int] = None
    duration: Optional[int] = None
    status: Optional[str] = None


class ProductGetResponse(BaseModel):
    id: int
    name: str
    content: str
    bid_price: int
    duration: int
    status: str
    modify: bool
    grade: str
    category: str
    is_approved: bool
    winner_user_id: int | None
    winner_nickname: str | None
    winner_bid_price: float | None
