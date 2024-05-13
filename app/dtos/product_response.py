from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    content: str
    bid_price: int
    duration: int
    user_id: int
    status: str
    modify: bool
    grade: str
    category: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str
    content: str
    bid_price: int
    duration: int
    status: str


class ProductOut(ProductBase):
    id: int
    status: str
    modify: bool
    grade: str
    category: str
