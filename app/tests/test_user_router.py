from unittest.mock import MagicMock, patch

from tortoise.contrib.test import TestCase

from app.dtos.user_response import SendVerificationCodeResponse
from app.services.user_service import (
    generate_verification_code,
    send_verification_email,
)


class TestEmailVerification(TestCase):

    def test_generate_verification_code(self) -> None:
        code1: int = generate_verification_code()
        code2: int = generate_verification_code()

        self.assertNotEqual(code1, code2)

    async def test_send_email(self) -> None:

        gmail_username: str = "its.verified.test@gmail.com"
        gmail_password: str = "goxvdsfjrovuyqzv"

        receiver_name = "TestUser"
        receiver_email = "example@example.com"

        request_data = SendVerificationCodeResponse(name=receiver_name, email=receiver_email)

        smtp_mock = MagicMock()
        with patch("app.services.user_service.smtplib.SMTP_SSL") as mock_smtp:
            mock_smtp.return_value = smtp_mock

            await send_verification_email(request_data)

            mock_smtp.assert_called_once_with("smtp.gmail.com", 465)
            smtp_mock.login.assert_called_once_with(gmail_username, gmail_password)
            smtp_mock.sendmail.assert_called_once()
