from __future__ import annotations

from typing import Optional

from passlib.context import CryptContext  # type: ignore
from tortoise import fields
from tortoise.models import Model

from app.dtos.winner_response import WinnerCreateResponse
from app.models.auctions import Auction
from app.models.common import Common
from app.models.products import Product
from app.models.users import User


class Winner(Common, Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="winners")
    auction: fields.ForeignKeyRelation[Auction] = fields.ForeignKeyField("models.Auction", related_name="winners")
    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField("models.Product", related_name="winners")
    user_id: int
    auction_id: int
    product_id: int
    bid_price = fields.FloatField()

    class Meta:
        table = "winners"

    @classmethod
    async def get_by_winner(cls, product_id: int) -> Optional[Winner]:
        return await cls.filter(product_id=product_id).order_by("-created_at").first()

    @classmethod
    async def create_by_winner(cls, request_data: WinnerCreateResponse, current_user: int) -> Winner:
        return await cls.create(
            user_id=current_user,
            auction_id=request_data.auction_id,
            product_id=request_data.product_id,
            bid_price=request_data.bid_price,
        )
