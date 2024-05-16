from fastapi import APIRouter

from app.dtos.terms_response import TermIDResponse
from app.dtos.user_response import (
    SendVerificationCodeResponse,
    UserSignUpResponse,
    VerifyContactResponse,
    VerifyEmailResponse,
    VerifyNicknameResponse,
)
from app.services.user_service import (
    send_verification_email,
    service_code_authentication,
    service_contact_verification,
    service_nickname_verification,
    service_signup,
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
