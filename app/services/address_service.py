from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError, ValidationError

from app.dtos.address_response import (
    AddressCreateResponse,
    AddressGetResponse,
    AddressUpdateResponse,
)
from app.models.address import Address


async def service_get_all_address() -> list[AddressGetResponse]:
    addresses = await Address.get_all_by_address()
    if len(addresses) == 0:
        raise HTTPException(status_code=404, detail="주소를 찾을 수 없습니다.")
    return [
        AddressGetResponse(
            id=address.id,
            name=address.name,
            address=address.address,
            detail_address=address.detail_address,
            zip_code=address.zip_code,
            is_main=address.is_main,
            user_id=address.user_id,  # type: ignore
            created_at=address.created_at,
            updated_at=address.updated_at,
        )
        for address in addresses
    ]


async def service_get_by_address_id(address_id: int) -> AddressGetResponse:
    address = await Address.get_by_address_id(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="주소를 찾을 수 없습니다.")

    return AddressGetResponse(
        id=address.id,
        name=address.name,
        address=address.address,
        detail_address=address.detail_address,
        zip_code=address.zip_code,
        is_main=address.is_main,
        user_id=address.user_id,  # type: ignore
        created_at=address.created_at,
        updated_at=address.updated_at,
    )


async def service_create_address(request_data: AddressCreateResponse) -> None:
    try:
        existing_main_address = await Address.filter(user_id=request_data.user_id, is_main=True).first()

        if existing_main_address:
            existing_main_address.is_main = False
            await existing_main_address.save()

        await Address.create_by_address(request_data)
        raise HTTPException(status_code=201, detail="주소가 성공적으로 생성되었습니다.")
    except IntegrityError as e:
        # 데이터 검증 오류 또는 데이터 중복 오류 처리
        raise HTTPException(status_code=400, detail=f"데이터 검증 오류: {e}")


async def service_update_address(address_id: int, request_data: AddressUpdateResponse) -> AddressUpdateResponse:
    try:
        exists = await Address.get_by_address_id(address_id)
        if not exists:
            raise HTTPException(status_code=404, detail="주소 아이디 값이 없습니다")

        # 메인 주소를 다른 걸 픽 했을 때 원래 True 였던 메인은 False 로 Update
        if request_data.is_main:
            await Address.filter(user_id=exists.user_id, is_main=True).exclude(id=address_id).update(is_main=False)  # type: ignore

        # 만약에 처음 만들 때 is_main 은 디폴트 값이 True 지만 처음만 만들고 그 한개를 False 로 Update 틀 막을지 말지 상의 후 넣을 예정

        address = await Address.update_by_address(address_id, request_data)

        return AddressUpdateResponse(
            name=address.name,
            address=address.address,
            detail_address=address.detail_address,
            zip_code=address.zip_code,
            is_main=address.is_main,
        )
    except ValidationError as ve:
        # 유효하지 않은 데이터에 대한 처리
        raise HTTPException(status_code=400, detail=str(ve))


async def service_delete_address(address_id: int) -> None:
    try:
        await Address.delete_by_address(address_id)
        raise HTTPException(status_code=200, detail="주소가 성공적으로 삭제되었습니다.")
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="주소 아이디 값이 없습니다")
