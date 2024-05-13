from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.dtos.inspection_response import (
    InspectionCreateResponse,
    InspectionGetResponse,
    InspectionUpdateResponse,
)
from app.models.inspections import Inspection
from app.models.products import Product


async def service_get_all_inspection() -> list[InspectionGetResponse]:
    inspections = await Inspection.get_all_by_inspection()
    return [
        InspectionGetResponse(
            id=inspection.id,
            inspector=inspection.inspector,
            product_id=inspection.product_id,  # type: ignore
            inspection_count=inspection.inspection_count,
            created_at=inspection.created_at,
            updated_at=inspection.updated_at,
        )
        for inspection in inspections
    ]


async def service_get_detail_inspection(product_id: int) -> list[InspectionGetResponse]:
    try:
        inspections = await Inspection.get_by_inspection_detail(product_id=product_id)
        if not inspections:
            raise HTTPException(status_code=404, detail="Inspections not found")
        return [
            InspectionGetResponse(
                id=inspection.id,
                inspector=inspection.inspector,
                product_id=inspection.product_id,  # type: ignore
                inspection_count=inspection.inspection_count,
                created_at=inspection.created_at,
                updated_at=inspection.updated_at,
            )
            for inspection in inspections
        ]
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Inspections not found")


async def service_get_one_inspection(inspection_id: int) -> InspectionGetResponse:
    try:
        inspection = await Inspection.get_by_inspection_id(inspection_id)
        if inspection is None:
            raise HTTPException(status_code=404, detail="Inspection 아이디 값이 없습니다")

        return InspectionGetResponse(
            id=inspection.id,
            inspector=inspection.inspector,
            product_id=inspection.product_id,  # type: ignore
            inspection_count=inspection.inspection_count,
            created_at=inspection.created_at,
            updated_at=inspection.updated_at,
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Inspection을 찾을 수 없습니다.")


async def service_create_inspection(request_data: InspectionCreateResponse) -> InspectionCreateResponse:
    try:
        await Product.get_by_product_id(product_id=request_data.product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product 아이디 값이 없습니다")
    inspection = await Inspection.create_by_inspection(request_data)

    return InspectionCreateResponse(
        inspector=inspection.inspector,
        product_id=inspection.product_id,  # type: ignore
        inspection_count=inspection.inspection_count,
    )


async def service_update_inspection(
    inspection_id: int, request_data: InspectionUpdateResponse
) -> InspectionUpdateResponse:
    try:
        inspection = await Inspection.update_by_inspection(inspection_id, request_data)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="inspection 아이디 값이 없습니다")

    return InspectionUpdateResponse(inspector=inspection.inspector, inspection_count=inspection.inspection_count)
