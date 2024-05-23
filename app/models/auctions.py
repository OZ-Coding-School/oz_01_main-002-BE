from __future__ import annotations

from datetime import datetime, timedelta

from tortoise import fields
from tortoise.models import Model

from app.dtos.auction_response import AuctionCreate, AuctionUpdate
from app.models.common import Common
from app.models.products import Product


def get_default_end_time() -> datetime:
    return datetime.now() + timedelta(minutes=3)


class Auction(Common, Model):
    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
        "models.Product", related_name="products", on_delete=fields.CASCADE
    )
    status = fields.BooleanField(default=True)
    start_time = fields.DatetimeField(auto_now_add=True)
    end_time = fields.DatetimeField(default=get_default_end_time)
    charge = fields.IntField(default=0)
    product_id: int

    class Meta:
        table = "auctions"

    @classmethod
    async def calculate_charge(cls, bid_price: int) -> int:
        if bid_price < 300000:
            return 20000
        elif 300000 <= bid_price < 1000000:
            return 50000
        elif 1000000 <= bid_price < 3000000:
            return 100000
        elif 3000000 <= bid_price < 5000000:
            return 200000
        elif 5000000 <= bid_price < 10000000:
            return 500000
        elif 10000000 <= bid_price < 30000000:
            return 1000000
        elif 30000000 <= bid_price < 50000000:
            return 2000000
        elif 50000000 <= bid_price < 200000000:
            return 5000000
        elif 200000000 <= bid_price < 500000000:
            return 10000000
        else:
            return 20000000

    @classmethod
    async def get_bid_price(cls, product_id: int) -> int:
        product = await Product.get(id=product_id)
        return product.bid_price

    @classmethod
    async def get_all_by_auctions(cls) -> list[Auction]:
        return await cls.all()

    @classmethod
    async def get_by_auction_id(cls, auction_id: int) -> Auction:
        return await cls.get(id=auction_id)

    @classmethod
    async def create_auction(cls, auction_data: AuctionCreate, charge: int) -> Auction:
        return await cls.create(product_id=auction_data.product_id, charge=charge)

    @classmethod
    async def delete_auction_by_product_id(cls, auction_id: int) -> None:
        await cls.filter(id=auction_id).delete()

    @classmethod
    async def update_by_auction_id(cls, auction_id: int, request_data: AuctionUpdate) -> Auction:
        auction = await cls.get(id=auction_id)

        update_data = request_data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(auction, key, value)

        await auction.save()
        return auction
