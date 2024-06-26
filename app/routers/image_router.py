from fastapi import APIRouter, File, Form, UploadFile

from app.dtos.image_response import ImageClassificationResponse, ImageUrlResponse
from app.services.image_service import service_get_images, service_save_image

router = APIRouter(prefix="/api/v1/image", tags=["image"], redirect_slashes=False)


@router.post("/upload")
async def save_image(
    component: str = Form(...),
    target_id: int = Form(...),
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    file3: UploadFile = File(...),
) -> dict[str, str]:
    request_data = ImageClassificationResponse(component=component, target_id=target_id)
    return await service_save_image(file1, file2, file3, request_data)


@router.get("/{component}/{target_id}")
async def get_images(component: str, target_id: int) -> list[ImageUrlResponse]:
    return await service_get_images(component, target_id)
