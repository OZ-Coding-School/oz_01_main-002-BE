from fastapi import APIRouter

from app.dtos.payment_response import PaymentCreateResponse, PaymentGetResponse
from app.services.payment_service import service_create_payment, service_get_by_payment

router = APIRouter(prefix="/api/v1/payments", tags=["payment"], redirect_slashes=False)


@router.post("/")
async def router_create_payment(request_data: PaymentCreateResponse) -> None:
    return await service_create_payment(request_data)


@router.get("/{payment_id}/", response_model=PaymentGetResponse)
async def router_get_by_payment_id(payment_id: int) -> PaymentGetResponse:
    return await service_get_by_payment(payment_id)
