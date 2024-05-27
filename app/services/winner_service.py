from fastapi import HTTPException
from tortoise.exceptions import IntegrityError, ValidationError

from app.dtos.winner_response import WinnerCreateResponse, WinnerGetResponse
from app.models.users import User
from app.models.winners import Winner


async def service_get_by_winner(product_id: int) -> WinnerGetResponse:
    winner = await Winner.get_by_winner(product_id)
    if not winner:
        raise HTTPException(status_code=404, detail="낙찰자를 찾을 수 없습니다")
    user = await User.get_by_user_id(winner.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return WinnerGetResponse(
        auction_id=winner.auction_id,
        product_id=winner.product_id,
        bid_price=winner.bid_price,
        winner=user.nickname,
    )


async def service_create_winner(request_data: WinnerCreateResponse, current_user: int) -> None:
    try:
        existing_winner = await Winner.filter(
            product_id=request_data.product_id, bid_price=request_data.bid_price
        ).first()
        if existing_winner:
            raise IntegrityError("이미 존재하는 낙찰금입니다.")
        await Winner.create_by_winner(request_data, current_user)
        raise HTTPException(status_code=201, detail="주소가 성공적으로 생성되었습니다.")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"데이터베이스 무결성 오류: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"유효성 검사 오류: {str(e)}")
