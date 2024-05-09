from unittest.mock import MagicMock, patch

from tortoise.contrib.test import TestCase

from app.services.user_service import (
    generate_verification_code,
    send_verification_email,
)

GMAIL_USERNAME: str = "its.verified.test@gmail.com"
GMAIL_PASSWORD: str = "goxvdsfjrovuyqzv"


class TestEmailVerification(TestCase):

    def test_generate_verification_code(self) -> None:
        code1: int = generate_verification_code()
        code2: int = generate_verification_code()
        code3: int = generate_verification_code()
        code4: int = generate_verification_code()

        self.assertEqual(len(str(code1)), 6)
        self.assertEqual(len(str(code2)), 6)
        self.assertEqual(len(str(code3)), 6)
        self.assertEqual(len(str(code4)), 6)
