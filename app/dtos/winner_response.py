from pydantic import BaseModel


class WinnerBase(BaseModel):
    product_id: int
    auction_id: int
    bid_price: float


class WinnerGetResponse(WinnerBase):
    winner: str


class WinnerCreateResponse(WinnerBase):
    pass
