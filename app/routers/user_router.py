from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile

from app.dtos.terms_response import TermIDResponse
from app.dtos.user_response import (
    SendVerificationCodeResponse,
    UserCoinCreateResponse,
    UserGetProfileResponse,
    UserLoginResponse,
    UserSignUpResponse,
    UserUpdateProfileResponse,
    VerifyContactResponse,
    VerifyEmailResponse,
    VerifyNicknameResponse,
)
from app.services.user_service import (
    get_current_refresh,
    get_current_user,
    send_verification_email,
    service_code_authentication,
    service_contact_verification,
    service_create_coin,
    service_get_user_detail,
    service_login,
    service_nickname_verification,
    service_signup,
    service_token_refresh,
    service_update_user_detail,
)

router = APIRouter(prefix="/api/v1/users", tags=["User"], redirect_slashes=False)


@router.post("/email/send")
async def send_verification_code(request_data: SendVerificationCodeResponse) -> dict[str, str]:
    return await send_verification_email(request_data)


@router.post("/email/verify")
async def verify_verification_code(request_data: VerifyEmailResponse) -> dict[str, str]:
    return await service_code_authentication(request_data)


@router.post("/nickname/verify")
async def verify_nickname(request_data: VerifyNicknameResponse) -> dict[str, str]:
    return await service_nickname_verification(request_data)


@router.post("/")
async def signup(request_data: UserSignUpResponse, term_data: list[TermIDResponse]) -> dict[str, str]:
    return await service_signup(request_data, term_data)


@router.post("/contact/verify")
async def contact_verification(request_data: VerifyContactResponse) -> dict[str, str]:
    return await service_contact_verification(request_data)


@router.post("/login")
async def login_response(request_data: UserLoginResponse) -> dict[str, str]:
    result = await service_login(request_data)

    return result


@router.post("/refresh")
async def refresh_token(current_refresh: str = Depends(get_current_refresh)) -> dict[str, str]:
    return await service_token_refresh(current_refresh)


@router.put("/coin")
async def create_coin(request_data: UserCoinCreateResponse, current_user: int = Depends(get_current_user)) -> None:
    return await service_create_coin(request_data, current_user)


@router.get("/")
async def router_get_user_detail(current_user: int = Depends(get_current_user)) -> UserGetProfileResponse:
    return await service_get_user_detail(current_user)


@router.put("/")
async def router_update_user_detail(
    request_data: UserUpdateProfileResponse,
    file: Optional[UploadFile] = File(None),
    current_user: int = Depends(get_current_user),
) -> UserUpdateProfileResponse:
    return await service_update_user_detail(request_data, file, current_user)
