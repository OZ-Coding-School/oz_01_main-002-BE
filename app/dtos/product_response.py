from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    name: str
    content: str
    bid_price: int
    duration: int
    status: str
    modify: bool
    grade: str
    category: str
