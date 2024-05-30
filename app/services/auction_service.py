from datetime import timedelta

from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.dtos.auction_response import (
    AuctionCreate,
    AuctionGetResponse,
    AuctionResponse,
    AuctionUpdate,
)
from app.models.auctions import Auction
from app.models.categories import Category
from app.models.products import Product
from app.models.users import User
from app.services.image_service import service_get_images


async def service_create_auction(auction_data: AuctionCreate) -> AuctionCreate:
    try:
        product = await Product.get_by_product_id(product_id=auction_data.product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")

    bid_price = await Auction.get_bid_price(auction_data.product_id)
    charge = await Auction.calculate_charge(bid_price)

    auction = await Auction.create_auction(auction_data, charge=charge)
    auction.end_time = auction.start_time + timedelta(days=product.duration)
    await auction.save()
    return AuctionCreate(product_id=auction.product_id, charge=charge, final_price=auction_data.final_price)


async def service_get_all_auctions() -> list[AuctionResponse]:
    try:
        auctions = await Auction.get_all_by_auctions()
        auction_responses = []
        for auction in auctions:
            product = await Product.get(id=auction.product_id)
            category = await Category.get(id=product.category_id)
            images = await service_get_images("product", auction.product_id)
            if images is None:
                raise HTTPException(status_code=404, detail="image not found")
            image_urls = [img.url for img in images]
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
                images=image_urls,
            )
            auction_responses.append(auction_response)
        return auction_responses
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="product not found")


async def service_get_by_auction_id(auction_id: int) -> AuctionGetResponse:
    auction = await Auction.get_by_auction_id(auction_id)
    if auction:
        product = await Product.get(id=auction.product_id)
        category = await Category.get(id=product.category_id)
        user = await User.get(id=product.user_id)
        images = await service_get_images("product", auction.product_id)
        if images is None:
            raise HTTPException(status_code=404, detail="image not found")
        image_urls = [img.url for img in images]
        return AuctionGetResponse(
            id=auction.id,
            product_id=auction.product_id,
            product_name=product.name,
            product_bid_price=product.bid_price,
            product_grade=product.grade,
            product_content=product.content,
            is_active=auction.is_active,
            start_time=auction.start_time.isoformat(),
            end_time=auction.end_time.isoformat(),
            status=auction.status,
            charge=auction.charge,
            category=category.name,
            final_price=auction.final_price,
            user_nickname=user.nickname,
            user_content=user.content,
            images=image_urls,
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

    return AuctionUpdate(status=new_auction.status, is_active=new_auction.is_active)


async def service_get_auctions_by_category_id(category_id: int) -> list[AuctionGetResponse]:
    products = await Product.filter(category_id=category_id).all()

    if not products:
        raise HTTPException(status_code=404, detail="Products not found for the given category ID")

    auctions_out = []

    for product in products:
        auction = await Auction.filter(product_id=product.id).first()

        if auction:
            category = await Category.get(id=product.category_id)
            user = await User.get(id=product.user_id)
            images = await service_get_images("product", auction.product_id)
            if images is None:
                raise HTTPException(status_code=404, detail="image not found")
            image_urls = [img.url for img in images]

            auction_out = AuctionGetResponse(
                id=auction.id,
                product_id=auction.product_id,
                product_name=product.name,
                product_bid_price=product.bid_price,
                product_grade=product.grade,
                product_content=product.content,
                is_active=auction.is_active,
                start_time=auction.start_time.isoformat(),
                end_time=auction.end_time.isoformat(),
                status=auction.status,
                charge=auction.charge,
                category=category.name,
                final_price=auction.final_price,
                user_nickname=user.nickname,
                user_content=user.content,
                images=image_urls,
            )
            auctions_out.append(auction_out)

    return auctions_out
