from fastapi import APIRouter, Depends

from app.dtos.winner_response import WinnerCreateResponse, WinnerGetResponse
from app.services.user_service import get_current_user
from app.services.winner_service import service_create_winner, service_get_by_winner

router = APIRouter(prefix="/api/v1/winners", tags=["winner"], redirect_slashes=False)


@router.get("/{product_id}", response_model=WinnerGetResponse)
async def router_get_by_winner(product_id: int, _: int = Depends(get_current_user)) -> WinnerGetResponse:
    return await service_get_by_winner(product_id)


@router.post("/", response_model=WinnerCreateResponse)
async def router_create_winner(
    request_data: WinnerCreateResponse, current_user: int = Depends(get_current_user)
) -> None:
    return await service_create_winner(request_data, current_user)
