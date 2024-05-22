from fastapi import APIRouter, Depends, Response

from app.dtos.terms_response import TermIDResponse
from app.dtos.user_response import (
    SendVerificationCodeResponse,
    TokenResponse,
    UserCoinCreateResponse,
    UserLoginResponse,
    UserSignUpResponse,
    VerifyContactResponse,
    VerifyEmailResponse,
    VerifyNicknameResponse,
)
from app.services.user_service import (
    get_current_user,
    send_verification_email,
    service_check_token,
    service_code_authentication,
    service_contact_verification,
    service_create_coin,
    service_login,
    service_nickname_verification,
    service_signup,
    service_token_refresh,
)

router = APIRouter(prefix="/api/v1/users", tags=["User"], redirect_slashes=False)


@router.post("/email/send")
async def send_verification_code(request_data: SendVerificationCodeResponse) -> dict[str, str]:
    return await send_verification_email(request_data)


@router.post("/email/verify")
async def verify_verification_code(request_data: VerifyEmailResponse) -> None:
    return await service_code_authentication(request_data)


@router.post("/nickname/verify")
async def verify_nickname(request_data: VerifyNicknameResponse) -> None:
    return await service_nickname_verification(request_data)


@router.post("/")
async def signup(request_data: UserSignUpResponse, term_data: list[TermIDResponse]) -> None:
    return await service_signup(request_data, term_data)


@router.post("/contact/verify")
async def contact_verification(request_data: VerifyContactResponse) -> None:
    return await service_contact_verification(request_data)


@router.post("/login")
async def login_response(request_data: UserLoginResponse, response: Response) -> dict[str, str]:
    result, refresh_token = await service_login(request_data)
    response.set_cookie(key="refresh_token", value=refresh_token)

    return result


@router.post("/refresh")
async def refresh_token(request_data: TokenResponse) -> dict[str, str]:
    return await service_token_refresh(request_data)


@router.post("/check/token")
async def check_token(request_data: TokenResponse) -> None:
    return await service_check_token(request_data)


@router.put("/coin")
async def create_coin(request_data: UserCoinCreateResponse, current_user: int = Depends(get_current_user)) -> None:
    return await service_create_coin(request_data, current_user)
