from tortoise import fields
from tortoise.models import Model

from app.dtos.image_response import (
    ImageComponentResponse,
    ImageResponse,
    ImageUrlResponse,
)
from app.models.common import Common


class Image(Model, Common):
    component = fields.CharField(max_length=10)
    target_id = fields.IntField()
    description = fields.TextField()
    url = fields.TextField()

    class Meta:
        table = "images"

    @classmethod
    async def get_by_target_id(cls, component: str, target_id: int) -> list["Image"]:
        return await cls.filter(component=component, target_id=target_id).order_by("created_at").all()

    @classmethod
    async def create_image(cls, request_data: ImageResponse) -> dict[str, str]:
        await cls.create(
            component=request_data.component,
            target_id=request_data.target_id,
            description=request_data.description,
            url=request_data.url,
        )
        return {"message": f"{request_data.component} image is save to s3"}
