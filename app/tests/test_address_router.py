from typing import Any

from httpx import AsyncClient
from passlib.context import CryptContext  # type: ignore
from tortoise.contrib.test import TestCase

from app import app
from app.models.address import Address
from app.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestAuthentication(TestCase):

    # 패스워드 해싱 함수
    @staticmethod
    def hash_password(password: str) -> Any:
        return pwd_context.hash(password)

    async def create_test_user(self) -> User:
        # 테스트를 위한 사용자 생성
        return await User.create(
            name="test_user",
            email="test@example.com",
            password=self.hash_password("test_password"),
            gender="male",
            age=30,
            contact="01012345678",
            nickname="test_nick",
            content="test_content",
            is_active=True,
        )

    async def test_router_create_address(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await self.create_test_user()

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}
            res = await ac.post("/api/v1/users/login", json=login_data)

            assert res.status_code == 200

            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            # 주소 생성 데이터 설정
            address_data = {
                "name": "test_address",
                "user_id": test_user.id,
                "address": "test_address",
                "detail_address": "test_detail_address",
                "zip_code": "test_zip_code",
                "is_main": True,
            }

            # 주소 생성 요청
            response = await ac.post("/api/v1/address/", json=address_data, headers=headers)
            assert response.status_code == 201  # HTTP 상태 코드 201 Created 확인

    async def test_router_get_all_address(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await self.create_test_user()

            # 사용자를 위해 주소를 생성합니다.
            await Address.create(
                name="test_address",
                user_id=user_test.id,
                address="test_address",
                detail_address="test_detail_address",
                zip_code="test_zip_code",
                is_main=True,
            )

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}  # 실제 패스워드를 사용합니다.
            res = await ac.post("/api/v1/users/login", json=login_data)
            assert res.status_code == 200  # HTTP 상태 코드 200 OK 확인
            token = res.json().get("access_token")

            headers = {"Authorization": f"Bearer {token}"}
            response = await ac.get("/api/v1/address/", headers=headers)
            assert response.status_code == 200
            response_data = response.json()
            assert len(response_data) == 1
            assert response_data[0]["name"] == "test_address"
            assert response_data[0]["address"] == "test_address"
            assert response_data[0]["detail_address"] == "test_detail_address"

    async def test_router_get_by_address_id(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await self.create_test_user()

            address = await Address.create(
                name="test_address",
                user_id=user_test.id,
                address="test_address",
                detail_address="test_detail_address",
                zip_code="test_zip_code",
                is_main=True,
            )
            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}  # 실제 패스워드를 사용합니다.
            res = await ac.post("/api/v1/users/login", json=login_data)
            assert res.status_code == 200  # HTTP 상태 코드 200 OK 확인
            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            response = await ac.get(f"/api/v1/address/{address.id}", headers=headers)
            assert response.status_code == 200  # HTTP 상태 코드 200 OK 확인
            response_data = response.json()
            assert response_data["name"] == "test_address"
            assert response_data["address"] == "test_address"
            assert response_data["detail_address"] == "test_detail_address"

    async def test_router_update_address(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await self.create_test_user()
            test_address = await Address.create(
                name="test_address",
                user_id=test_user.id,
                address="test_address",
                detail_address="test_detail_address",
                zip_code="test_zip_code",
                is_main=True,
            )

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}  # 실제 패스워드를 사용합니다.
            res = await ac.post("/api/v1/users/login", json=login_data)
            assert res.status_code == 200  # HTTP 상태 코드 200 OK 확인
            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            address_data = {
                "name": "test_address1",
                "user_id": test_user.id,
                "address": "test_address2",
                "detail_address": "test_detail_address3",
                "zip_code": "test_zip_code4",
                "is_main": False,
            }
            response = await ac.put(f"/api/v1/address/{test_address.id}", json=address_data, headers=headers)
            assert response.status_code == 200  # HTTP 상태 코드 200 OK 확인
            response_data = response.json()
            print(response_data)
            assert response_data["name"] == "test_address1"
            assert response_data["address"] == "test_address2"
            assert response_data["detail_address"] == "test_detail_address3"
            assert response_data["zip_code"] == "test_zip_code4"
            assert response_data["is_main"] == False

    async def test_service_delete_address(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await self.create_test_user()
            test_address = await Address.create(
                name="test_address",
                user_id=test_user.id,
                address="test_address",
                detail_address="test_detail_address",
                zip_code="test_zip_code",
                is_main=True,
            )
            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}  # 실제 패스워드를 사용합니다.
            res = await ac.post("/api/v1/users/login", json=login_data)
            assert res.status_code == 200  # HTTP 상태 코드 200 OK 확인
            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            response = await ac.delete(f"/api/v1/address/{test_address.id}", headers=headers)
            assert response.status_code == 200  # HTTP 상태 코드 200 OK 확인
