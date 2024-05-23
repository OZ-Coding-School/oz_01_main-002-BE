from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, ValidationError

from app.dtos.carries_response import (
    CarriesCreateResponse,
    CarriesGetResponse,
    CarriesUpdateResponse,
)
from app.models.carries import Carries


async def service_get_all_carries() -> list[CarriesGetResponse]:
    carries = await Carries.get_all_by_carries()
    if len(carries) == 0:
        raise HTTPException(status_code=404, detail="carries 아이디 값이 없습니다")
    return [
        CarriesGetResponse(
            id=carry.id,
            product_id=carry.product_id,
            address=carry.address,
            sender=carry.sender,
            contact=carry.contact,
            size=carry.size,
            amount=carry.amount,
            created_at=carry.created_at,
            updated_at=carry.updated_at,
        )
        for carry in carries
    ]


async def service_get_by_carries_id(carries_id: int) -> CarriesGetResponse:
    carry = await Carries.get_by_carries_id(carries_id)
    if not carry:
        raise HTTPException(status_code=404, detail="carries 아이디 값이 없습니다")

    return CarriesGetResponse(
        id=carry.id,
        product_id=carry.product_id,
        address=carry.address,
        sender=carry.sender,
        contact=carry.contact,
        size=carry.size,
        amount=carry.amount,
        created_at=carry.created_at,
        updated_at=carry.updated_at,
    )


async def service_create_carries(request_data: CarriesCreateResponse) -> None:
    try:
        carry = await Carries.create_by_carries(request_data)

        if carry:
            # 성공 메시지와 상태 코드 반환
            raise HTTPException(status_code=201, detail="Carries 성공적으로 생성되었습니다.")
        else:
            # 검수 생성 실패 시 HTTP 예외 발생
            raise HTTPException(status_code=500, detail="Carries 생성에 실패했습니다.")
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))


async def service_update_carries(carries_id: int, request_data: CarriesUpdateResponse) -> CarriesUpdateResponse:
    try:
        exists = await Carries.get_by_carries_id(carries_id)
        if not exists:
            raise HTTPException(status_code=404, detail="Carries 아이디 값이 없습니다.")

        carry = await Carries.update_by_carries(carries_id, request_data)

        return CarriesUpdateResponse(
            address=carry.address,
            sender=carry.sender,
            contact=carry.contact,
            size=carry.size,
            amount=carry.amount,
            created_at=carry.created_at,
            updated_at=carry.updated_at,
        )
    except ValidationError as ve:
        # 유효하지 않은 데이터에 대한 처리
        raise HTTPException(status_code=422, detail=str(ve))


async def service_delete_carries(carries_id: int) -> None:
    try:
        await Carries.delete_by_carries(carries_id)
        raise HTTPException(status_code=200, detail="Carries가 성공적으로 삭제되었습니다.")
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Carries 아이디 값이 없습니다.")
