from pydantic import BaseModel


class ImageClassificationResponse(BaseModel):
    component: str
    target_id: int


class ImageResponse(ImageClassificationResponse):
    description: str
    url: str


class ImageComponentResponse(BaseModel):
    component: str
    target_id: int


class ImageUrlResponse(BaseModel):
    url: str


class ProductImageResponse(BaseModel):
    description: str
