from datetime import datetime
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.dtos.payment_response import (
    PaymentCreateGetResponse,
    PaymentCreateResponse,
    PaymentGetResponse,
    ProductBase,
)
from app.models.address import Address
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


async def service_create_payment(request_data: PaymentCreateResponse, current_user: int) -> PaymentCreateGetResponse:
    try:
        user = await User.get(id=current_user)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    products = []  # 상품 객체를 저장할 리스트
    total_product_amount = 0  # 상품 가격 합계 초기화

    for product_id in request_data.product_ids:
        try:
            product = await Product.get(id=product_id)
            products.append(ProductBase(id=product.id, name=product.name, bid_price=product.bid_price))
            total_product_amount += product.bid_price
        except DoesNotExist:
            raise HTTPException(status_code=404, detail=f"상품 ID {product_id}를 찾을 수 없습니다")

    if user.coin < request_data.total_amount:
        raise HTTPException(status_code=400, detail="코인 잔액이 부족합니다")

    user.coin -= request_data.total_amount
    await user.save()

    try:
        main_address = await Address.get_main_address_by_user_id(current_user)
        if not main_address:
            raise HTTPException(status_code=404, detail="주요 주소를 찾을 수 없습니다")

        if total_product_amount != request_data.total_amount:
            raise HTTPException(
                status_code=400,
                detail=f"상품 총 금액 합계와 요청된 총 금액이 일치하지 않습니다. (상품 총 금액 합계: {total_product_amount}, 요청된 총 금액: {request_data.total_amount})"
            )

        uuid = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        payment = await Payment.create_by_payment(request_data, current_user)

        return PaymentCreateGetResponse(
            id=payment.id,
            user_id=user.id,
            products=products,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
            total_amount=payment.total_amount,
            uuid=uuid,
            receiver_name=user.name,
            receiver_address=f"{main_address.address}, {main_address.detail_address}, {main_address.zip_code}",
            user_coin=user.coin,
        )
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"데이터베이스 오류: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"유효하지 않은 값: {str(e)}")
