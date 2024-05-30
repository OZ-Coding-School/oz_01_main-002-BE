import datetime
import uuid

from botocore.exceptions import NoCredentialsError  # type: ignore
from fastapi import HTTPException, UploadFile

from app.configs import settings
from app.dtos.image_response import (
    ImageClassificationResponse,
    ImageResponse,
    ImageUrlResponse,
)
from app.models.images import Image
from app.utils.s3_ import s3_client

s3 = s3_client()
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/gif"]


async def service_upload_image(file: UploadFile, folder: str) -> str:
    await file.seek(0)

    file_contents = await file.read()
    file_size = len(file_contents)

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if file.content_type:
        file_type = "." + file.content_type.split("/")[-1]
    else:
        file_type = ".jpg"

    filename = str(current_time) + str(uuid.uuid4().hex) + file_type

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the allowed limit of 5MB")

    if file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        s3_key = f"{folder}/{filename}"

        s3.put_object(Bucket=settings.AWS_S3_BUCKET_NAME, Key=s3_key, Body=file_contents, ContentType=file.content_type)  # type: ignore

        s3_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"  # type: ignore
        return s3_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def service_save_image(file: UploadFile, request_data: ImageClassificationResponse) -> dict[str, str]:
    url = await service_upload_image(file, request_data.component)
    image_data = ImageResponse(
        component=request_data.component,
        target_id=request_data.target_id,
        description=file.filename,
        url=url,
    )
    return await Image.create_image(request_data=image_data)


async def service_get_images(component: str, target_id: int) -> list[ImageUrlResponse]:
    image_data = await Image.get_by_target_id(component, target_id)
    return [ImageUrlResponse(url=i.url) for i in image_data]
