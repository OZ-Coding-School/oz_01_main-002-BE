from fastapi import APIRouter

from app.dtos.user_response import SendVerificationCodeResponse
from app.services.user_service import send_verification_email

router = APIRouter(prefix="/api/v1/users", tags=["User"], redirect_slashes=False)


@router.post("/email/send")
async def send_verification_code(request_data: SendVerificationCodeResponse) -> dict[str, str]:
    return send_verification_email(request_data)
