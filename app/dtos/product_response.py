from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    bid_price: Optional[int] = None
    duration: Optional[int] = None
    user_id: int
    status: Optional[str] = None
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


class ProductOut(ProductBase):
    id: int
    status: str
    modify: bool
    grade: str
    category_id: int


class ProductGetResponse(BaseModel):
    name: str
    content: str
    bid_price: int
    duration: int
    status: str
    modify: bool
    grade: str
    category: str
    is_approved: bool
