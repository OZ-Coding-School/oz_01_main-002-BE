from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.dtos.payment_response import PaymentCreateResponse
from app.models.common import Common
from app.models.products import Product
from app.models.users import User


class Payment(Common, Model):

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="payment", on_delete=fields.CASCADE
    )
    user_id: int
    products: fields.ManyToManyRelation[Product] = fields.ManyToManyField("models.Product", related_name="payments")
    total_amount = fields.FloatField()

    class Meta:
        table = "payments"

    @classmethod
    async def get_by_payments_id(cls, payment_id: int) -> Payment:
        return await cls.get(id=payment_id).prefetch_related("products")

    @classmethod
    async def create_by_payment(cls, request_data: PaymentCreateResponse) -> Payment:
        payment = await cls.create(user_id=request_data.user_id, total_amount=request_data.total_amount)

        products = await Product.filter(id__in=request_data.product_ids)
        await payment.products.add(*products)
        return payment
