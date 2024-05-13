from pydantic import BaseModel


class CategoryBaseResponse(BaseModel):
    item_id: int
    parent_id: int
    sqe: int
    name: str


class CategoryResponse(CategoryBaseResponse):
    id: int
