from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.dtos.payment_response import (
    PaymentCreateResponse,
    PaymentGetResponse,
    ProductBase,
)
from app.models.payments import Payment
from app.models.products import Product
from app.models.users import User


async def service_get_by_payment(payment_id: int) -> PaymentGetResponse:
    try:
        payment = await Payment.get_by_payments_id(payment_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Payment 아이디 값이 없습니다.")

    products = [
        ProductBase(id=product.id, name=product.name, bid_price=product.bid_price) for product in payment.products
    ]

    return PaymentGetResponse(
        id=payment.id,
        user_id=payment.user_id,
        products=products,
        created_at=payment.created_at,
        updated_at=payment.updated_at,
        total_amount=payment.total_amount,
    )


async def service_create_payment(request_data: PaymentCreateResponse, current_user: int) -> None:
    try:
        await User.get(id=current_user)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User 없습니다.")

    for product_id in [product for product in request_data.product_ids]:
        try:
            await Product.get(id=product_id)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail=f"Product ID {product_id}이(가) 없습니다.")

    try:
        # Todo  유저가 가지고있는 돈과 products돈 뺴줘서 업데이트 하기 추후에 넣을 예정

        payment = await Payment.create_by_payment(request_data, current_user)
        if payment:
            # 성공 메시지와 상태 코드 반환
            raise HTTPException(status_code=201, detail="payment 성공적으로 생성되었습니다.")
        else:
            # 검수 생성 실패 시 HTTP 예외 발생
            raise HTTPException(status_code=500, detail="payment 생성에 실패했습니다.")
    except IntegrityError as e:
        # 데이터베이스 무결성 오류 처리 (예: 중복 키, 외래 키 제약 조건 위반 등)
        raise HTTPException(status_code=400, detail=f"데이터베이스 오류: {str(e)}")
    except ValueError as e:
        # 값 오류 처리 (예: 유효하지 않은 데이터 형식 등)
        raise HTTPException(status_code=400, detail=f"유효하지 않은 값: {str(e)}")
