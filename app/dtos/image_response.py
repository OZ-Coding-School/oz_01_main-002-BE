from pydantic import BaseModel


class ImageClassificationResponse(BaseModel):
    component: str
    target_id: int
    description: str


class ImageResponse(ImageClassificationResponse):
    url: str


class ImageComponentResponse(BaseModel):
    component: str
    target_id: int


class ImageUrlResponse(BaseModel):
    url: str
