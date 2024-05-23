from unittest.mock import MagicMock, patch

from httpx import AsyncClient
from tortoise.contrib.test import TestCase

from app import app
from app.configs import settings
from app.dtos.user_response import SendVerificationCodeResponse
from app.models.users import User
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

        gmail_username: str = settings.GMAIL_USERNAME
        gmail_password: str = settings.GMAIL_PASSWORD

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

    async def test_nickname_verification(self) -> None:
        await User.create(
            name="test_user",
            email="test@example.com",
            password="password123",
            gender=123,
            age=123,
            contact="abc",
            nickname="test",
            content="content",
        )
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("api/v1/users/nickname/verify", json={"nickname": "test"})
            response2 = await ac.post("api/v1/users/nickname/verify", json={"nickname": "test2"})
            response3 = await ac.post("api/v1/users/nickname/verify", json={"nickname": "123"})

            assert response.status_code == 400
            assert response2.status_code == 200
            assert response3.status_code == 400
