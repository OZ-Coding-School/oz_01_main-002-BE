import asyncio
from typing import Any

import orjson
import redis
from httpx import AsyncClient
from passlib.context import CryptContext  # type: ignore
from tortoise.contrib.test import TestCase

from app import app
from app.models.terms import Terms
from app.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestUserRouter(TestCase):
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
            contact="01099999999",
            nickname="nick",
            content="sdwdw",
        )

    @staticmethod
    async def generate_verification_code() -> str:
        # 예시 코드 생성 함수
        return "123456"

    async def test_send_verification_code(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:

            data = {"email": "test@example.com"}
            response = await ac.post("/api/v1/users/email/send", json=data)

            assert response.status_code == 200

    async def test_verify_verification_code(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)
            loop = asyncio.get_event_loop()
            verification_code = await self.generate_verification_code()

            # Redis에 인증 코드를 미리 설정
            email = "test@example.com"

            # 동기 함수를 비동기적으로 실행
            await loop.run_in_executor(
                None, redis_client.set, email, orjson.dumps({"email": email, "code": str(verification_code)})
            )
            await loop.run_in_executor(None, redis_client.expire, email, 60)

            data = {"email": "test@example.com", "code": verification_code}
            response = await ac.post("/api/v1/users/email/verify", json=data)

            assert response.status_code == 200

    #
    async def test_verify_nickname(self) -> None:
        await self.create_test_user()
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("api/v1/users/nickname/verify", json={"nickname": "nick"})
            response1 = await ac.post("api/v1/users/nickname/verify", json={"nickname": "nick1"})
            assert response.status_code == 400
            assert response1.status_code == 200

    async def test_signup(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            term = await Terms.create(
                name="test_term",
                content="test_content",
            )
            data = {
                "request_data": {
                    "name": "test_name",
                    "email": "test_email",
                    "password": "test_password",
                    "gender": "남성",
                    "age": 27,
                    "contact": "test_contact",
                    "nickname": "test_nickname",
                },
                "term_data": [{"id": term.id}],
            }
            response = await ac.post("api/v1/users/", json=data)
            assert response.status_code == 201

    async def test_contact_verification(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await self.create_test_user()
            response = await ac.post("api/v1/users/contact/verify", json={"contact": "010-9999-9999"})
            assert response.status_code == 200

    async def test_login_response(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await self.create_test_user()
            data = {"email": "test@example.com", "password": "test_password"}
            response = await ac.post("/api/v1/users/login", json=data)
            assert response.status_code == 200

    async def test_refresh_token(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await self.create_test_user()

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}
            res = await ac.post("/api/v1/users/login", json=login_data)

            assert res.status_code == 200

            refresh_token = res.cookies.get("refresh_token")
            headers = {"Authorization": f"Bearer {refresh_token}"}

            response = await ac.post("/api/v1/users/refresh", headers=headers)
            assert response.status_code == 200

    async def test_create_coin(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await self.create_test_user()

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}
            res = await ac.post("/api/v1/users/login", json=login_data)

            assert res.status_code == 200

            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            response = await ac.put("/api/v1/users/coin", json={"coin": "10000"}, headers=headers)
            assert response.status_code == 200

    async def test_router_get_user_detail(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await self.create_test_user()

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}
            res = await ac.post("/api/v1/users/login", json=login_data)

            assert res.status_code == 200

            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            response = await ac.get("/api/v1/users/", headers=headers)
            assert response.status_code == 200

    async def test_router_update_user_detail(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await self.create_test_user()

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}
            res = await ac.post("/api/v1/users/login", json=login_data)

            assert res.status_code == 200

            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            data = {"nickname": "카와이", "contact": "010-1234-5678", "content": "없음"}

            response = await ac.put("/api/v1/users/", json=data, headers=headers)
            assert response.status_code == 200
