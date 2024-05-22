from typing import Any

from httpx import AsyncClient
from passlib.context import CryptContext  # type: ignore
from tortoise.contrib.test import TestCase

from app import app
from app.models.terms import Terms
from app.models.terms_agreements import TermsAgreement
from app.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestTermAgreementRouter(TestCase):
    @staticmethod
    def hash_password(password: str) -> Any:
        return pwd_context.hash(password)

    async def create_test_user(self) -> User:
        return await User.create(
            name="test_user",
            email="test@example.com",
            password=self.hash_password("test_password"),
            gender="남",
            age=12,
            contact="test",
            nickname="nick",
            content="sdwdw",
        )

    @staticmethod
    async def create_test_terms() -> Terms:
        return await Terms.create(
            id=1,
            name="이용약관",
            content="약관 내용",
            is_required=True,
            is_active=True,
        )

    async def test_router_get_by_all_term_agreement(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # given
            user_test = await self.create_test_user()
            term_test = await self.create_test_terms()

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}
            res = await ac.post("/api/v1/users/login", json=login_data)

            assert res.status_code == 200

            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            await TermsAgreement.create(
                user_id=user_test.id,
                term_id=term_test.id,
            )
            await TermsAgreement.create(
                user_id=user_test.id,
                term_id=term_test.id,
            )
            response = await ac.get("/api/v1/terms_agreement/", headers=headers)

            assert response.status_code == 200
            # then
            response_data = response.json()
            assert len(response_data) == 2

            assert response_data[0]["user_id"] == user_test.id
            assert response_data[0]["term_id"] == term_test.id

            assert response_data[1]["user_id"] == user_test.id
            assert response_data[1]["term_id"] == term_test.id

    async def test_router_create_term_agreement(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await self.create_test_user()
            term_test = await self.create_test_terms()

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}
            res = await ac.post("/api/v1/users/login", json=login_data)

            assert res.status_code == 200

            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            data = {
                "user_id": user_test.id,
                "term_id": term_test.id,
            }
            response = await ac.post("/api/v1/terms_agreement/", json=data, headers=headers)
            assert response.status_code == 201
