from fastapi import APIRouter

from app.dtos.user_response import (
    SendVerificationCodeResponse,
    VerifyEmailResponse,
    VerifyNicknameResponse,
)
from app.services.user_service import (
    send_verification_email,
    service_code_authentication,
    service_nickname_verification,
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
