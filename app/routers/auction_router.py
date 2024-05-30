from fastapi import APIRouter

from app.dtos.auction_response import (
    AuctionCreate,
    AuctionGetResponse,
    AuctionResponse,
    AuctionUpdate,
)
from app.models.auctions import Auction
from app.services.auction_service import (
    service_create_auction,
    service_delete_auction_by_id,
    service_get_all_auctions,
    service_get_auctions_by_category_id,
    service_get_by_auction_id,
    service_update_auction,
)

router = APIRouter(prefix="/api/v1/auctions", tags=["auction"], redirect_slashes=False)


@router.get("/", response_model=list[AuctionResponse])
async def router_get_auctions() -> list[AuctionResponse]:
    return await service_get_all_auctions()


@router.post("/", response_model=AuctionCreate)
async def router_create_auction(auction_data: AuctionCreate) -> AuctionCreate:
    bid_price = await Auction.get_bid_price(auction_data.product_id)
    charge = await Auction.calculate_charge(bid_price)
    auction_data.charge = charge
    return await service_create_auction(auction_data)


@router.get("/{auction_id}", response_model=AuctionGetResponse)
async def router_get_product_id(auction_id: int) -> AuctionGetResponse:
    return await service_get_by_auction_id(auction_id)


@router.delete("/{auction_id}")
async def router_delete_auction_by_id(auction_id: int) -> dict[str, str]:
    await service_delete_auction_by_id(auction_id)
    return {"message": "Auction deleted successfully"}


@router.put("/{auction_id}", response_model=AuctionUpdate)
async def router_update_auction(auction_id: int, request_data: AuctionUpdate) -> AuctionUpdate:
    return await service_update_auction(auction_id, request_data)


@router.get("/categories/{category_id}", response_model=list[AuctionGetResponse])
async def router_get_auctions_by_category_id(category_id: int) -> list[AuctionGetResponse]:
    return await service_get_auctions_by_category_id(category_id)
