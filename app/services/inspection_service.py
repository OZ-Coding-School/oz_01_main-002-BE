from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, ValidationError

from app.dtos.inspection_response import (
    InspectionCreateResponse,
    InspectionGetResponse,
    InspectionUpdateResponse,
)
from app.models.inspections import Inspection
from app.models.products import Product


async def service_get_all_inspection() -> list[InspectionGetResponse]:
    inspections = await Inspection.get_all_by_inspection()
    if len(inspections) == 0:
        raise HTTPException(status_code=404, detail="Inspection 아이디 값이 없습니다.")
    return [
        InspectionGetResponse(
            id=inspection.id,
            inspector=inspection.inspector,
            product_id=inspection.product_id,
            created_at=inspection.created_at,
            updated_at=inspection.updated_at,
        )
        for inspection in inspections
    ]


async def service_get_detail_inspection(product_id: int) -> list[InspectionGetResponse]:
    inspections = await Inspection.get_by_inspection_detail(product_id=product_id)
    if not inspections:
        raise HTTPException(status_code=404, detail="Inspection 아이디 값이 없습니다.")
    return [
        InspectionGetResponse(
            id=inspection.id,
            inspector=inspection.inspector,
            product_id=inspection.product_id,
            created_at=inspection.created_at,
            updated_at=inspection.updated_at,
        )
        for inspection in inspections
    ]


async def service_get_one_inspection(inspection_id: int) -> InspectionGetResponse:
    inspection = await Inspection.get_by_inspection_id(inspection_id)
    if inspection is None:
        raise HTTPException(status_code=404, detail="Inspection 아이디 값이 없습니다.")

    return InspectionGetResponse(
        id=inspection.id,
        inspector=inspection.inspector,
        product_id=inspection.product_id,
        created_at=inspection.created_at,
        updated_at=inspection.updated_at,
    )


async def service_create_inspection(request_data: InspectionCreateResponse) -> None:
    try:
        product = await Product.get_by_product_id(product_id=request_data.product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product 아이디 값이 없습니다")
        product.is_approved = True
        await product.save()

        inspection = await Inspection.create_by_inspection(request_data)

        if inspection:
            # 성공 메시지와 상태 코드 반환
            raise HTTPException(status_code=201, detail="Inspection 생성이 성공적으로 완료되었습니다.")
        else:
            # 검수 생성 실패 시 HTTP 예외 발생
            raise HTTPException(status_code=500, detail="Inspection 생성에 실패했습니다.")
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))


async def service_update_inspection(
    inspection_id: int, request_data: InspectionUpdateResponse
) -> InspectionUpdateResponse:
    try:
        inspection = await Inspection.update_by_inspection(inspection_id, request_data)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Inspection 아이디 값이 없습니다.")

    return InspectionUpdateResponse(inspector=inspection.inspector)
