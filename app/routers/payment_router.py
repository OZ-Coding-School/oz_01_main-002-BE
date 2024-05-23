from fastapi import APIRouter, Depends

from app.dtos.payment_response import (
    PaymentCreateGetResponse,
    PaymentCreateResponse,
    PaymentGetResponse,
)
from app.services.payment_service import service_create_payment, service_get_by_payment
from app.services.user_service import get_current_user

router = APIRouter(prefix="/api/v1/payments", tags=["payment"], redirect_slashes=False)


@router.post("/")
async def router_create_payment(
    request_data: PaymentCreateResponse, current_user: int = Depends(get_current_user)
) -> PaymentCreateGetResponse:
    return await service_create_payment(request_data, current_user)


@router.get("/{payment_id}/", response_model=PaymentGetResponse)
async def router_get_by_payment_id(payment_id: int, _: int = Depends(get_current_user)) -> PaymentGetResponse:
    return await service_get_by_payment(payment_id)
