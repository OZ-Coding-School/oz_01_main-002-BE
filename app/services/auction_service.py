from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.dtos.auction_response import AuctionCreate, AuctionResponse, AuctionUpdate
from app.models.auctions import Auction
from app.models.categories import Category
from app.models.products import Product


async def service_create_auction(auction_data: AuctionCreate) -> AuctionCreate:
    try:
        product = await Product.get_by_product_id(product_id=auction_data.product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")

    bid_price = await Auction.get_bid_price(auction_data.product_id)
    charge = await Auction.calculate_charge(bid_price)

    auction = await Auction.create_auction(auction_data, charge=charge, final_price=auction_data.final_price)
    return AuctionCreate(product_id=auction.product_id, charge=charge, final_price=auction_data.final_price)


async def service_get_all_auctions() -> list[AuctionResponse]:
    try:
        auctions = await Auction.get_all_by_auctions()
        auction_responses = []
        for auction in auctions:
            product = await Product.get(id=auction.product_id)
            category = await Category.get(id=product.category_id)
            auction_response = AuctionResponse(
                id=auction.id,
                product_id=auction.product_id,
                product_name=product.name,
                product_bid_price=product.bid_price,
                product_grade=product.grade,
                is_active=auction.is_active,
                start_time=auction.start_time.isoformat(),
                end_time=auction.end_time.isoformat(),
                status=auction.status,
                charge=auction.charge,
                category=category.name,
                final_price=auction.final_price,
            )
            auction_responses.append(auction_response)
        return auction_responses
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="product not found")


async def service_get_by_auction_id(auction_id: int) -> AuctionResponse:
    auction = await Auction.get_by_auction_id(auction_id)
    if auction:
        product = await Product.get(id=auction.product_id)
        category = await Category.get(id=product.category_id)
        return AuctionResponse(
            id=auction.id,
            product_id=auction.product_id,
            product_name=product.name,
            product_bid_price=product.bid_price,
            product_grade=product.grade,
            is_active=auction.is_active,
            start_time=auction.start_time.isoformat(),
            end_time=auction.end_time.isoformat(),
            status=auction.status,
            charge=auction.charge,
            category=category.name,
            final_price=auction.final_price,
        )
    raise HTTPException(status_code=404, detail="Product not found")


async def service_delete_auction_by_id(auction_id: int) -> None:
    try:
        auction = await Auction.get_by_auction_id(auction_id)
        await auction.delete()
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Auction not found")


async def service_update_auction(auction_id: int, auction_data: AuctionUpdate) -> AuctionUpdate:
    try:
        auction = await Auction.get_by_auction_id(auction_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="not found")

    new_auction = await Auction.update_by_auction_id(auction_id, auction_data)

    return AuctionUpdate(status=new_auction.status)
