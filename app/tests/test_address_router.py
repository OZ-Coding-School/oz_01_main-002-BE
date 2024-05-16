from httpx import AsyncClient
from tortoise.contrib.test import TestCase

from app import app
from app.models.address import Address
from app.models.users import User


class TestAddressRouter(TestCase):
    async def test_router_get_all_address(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await User.create(
                name="test_user",
                email="gudqls0516@naver.com",
                password="pw12345",
                gender="남",
                age=12,
                contact="test",
                nickname="nick",
                content="sdwdw",
            )
            await Address.create(
                name="test_address",
                user_id=user_test.id,
                address="test_address",
                detail_address="test_detail_address",
                zip_code="test_zip_code",
                is_main=True,
            )
            await Address.create(
                name="test_address1",
                user_id=user_test.id,
                address="test_address1",
                detail_address="test_detail_address1",
                zip_code="test_zip_code1",
                is_main=True,
            )

            response = await ac.get("/api/v1/address/")
            assert response.status_code == 200
            response_data = response.json()
            self.assertEqual(len(response_data), 2)
            assert response_data[0]["name"] == "test_address"
            assert response_data[0]["address"] == "test_address"
            assert response_data[0]["detail_address"] == "test_detail_address"
            assert response_data[0]["zip_code"] == "test_zip_code"
            assert response_data[0]["is_main"] == True

            assert response_data[1]["name"] == "test_address1"
            assert response_data[1]["address"] == "test_address1"
            assert response_data[1]["detail_address"] == "test_detail_address1"
            assert response_data[1]["zip_code"] == "test_zip_code1"
            assert response_data[1]["is_main"] == True

    async def test_router_get_by_address_id(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await User.create(
                name="test_user",
                email="gudqls0516@naver.com",
                password="pw12345",
                gender="남",
                age=12,
                contact="test",
                nickname="nick",
                content="sdwdw",
            )
            address = await Address.create(
                name="test_address",
                user_id=user_test.id,
                address="test_address",
                detail_address="test_detail_address",
                zip_code="test_zip_code",
                is_main=True,
            )
            response = await ac.get(f"api/v1/address/{address.id}")
            assert response.status_code == 200
            response_data = response.json()
            print(response_data)

            assert response_data["name"] == "test_address"
            assert response_data["address"] == "test_address"
            assert response_data["detail_address"] == "test_detail_address"
            assert response_data["zip_code"] == "test_zip_code"
            assert response_data["is_main"] == True

    async def test_router_create_address(self) -> None:
        # AsyncClient 생성
        async with AsyncClient(app=app, base_url="http://test") as ac:

            # 테스트용 사용자 생성
            test_user = await User.create(
                name="test_user",
                email="gudqls0516@naver.com",
                password="pw12345",
                gender="남",
                age=12,
                contact="test",
                nickname="nick",
                content="sdwdw",
            )
            data = {
                "name": "test_address",
                "user_id": test_user.id,  # 실제 사용자 ID로 대체해야 합니다.
                "address": "test_address",
                "detail_address": "test_detail_address",
                "zip_code": "test_zip_code",
                "is_main": True,
            }
            # POST 요청을 보내고 응답을 받습니다.
            response = await ac.post("/api/v1/address/", json=data)

            assert response.status_code == 201

    async def test_router_update_address(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:

            test_user = await User.create(
                name="test_user",
                email="gudqls0516@naver.com",
                password="pw12345",
                gender="남",
                age=12,
                contact="test",
                nickname="nick",
                content="sdwdw",
            )
            test_address = await Address.create(
                name="test_address",
                user_id=test_user.id,
                address="test_address",
                detail_address="test_detail_address",
                zip_code="test_zip_code",
                is_main=True,
            )
            data = {
                "name": "test_address1",
                "user_id": test_user.id,  # 실제 사용자 ID로 대체해야 합니다.
                "address": "test_address2",
                "detail_address": "test_detail_address3",
                "zip_code": "test_zip_code4",
                "is_main": False,
            }
            # POST 요청을 보내고 응답을 받습니다.
            response = await ac.put(f"/api/v1/address/{test_address.id}", json=data)

            assert response.status_code == 200
            response_data = response.json()

            assert response_data["name"] == data["name"]
            assert response_data["address"] == data["address"]
            assert response_data["detail_address"] == data["detail_address"]
            assert response_data["zip_code"] == data["zip_code"]
            assert response_data["is_main"] == data["is_main"]

    async def test_service_delete_address(self) -> None:
        # AsyncClient 생성
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # 테스트용 사용자 생성
            test_user = await User.create(
                name="test_user",
                email="gudqls0516@naver.com",
                password="pw12345",
                gender="남",
                age=12,
                contact="test",
                nickname="nick",
                content="sdwdw",
            )
            test_address = await Address.create(
                name="test_address",
                user_id=test_user.id,
                address="test_address",
                detail_address="test_detail_address",
                zip_code="test_zip_code",
                is_main=True,
            )
            response = await ac.delete(f"/api/v1/address/{test_address.id}")

            assert response.status_code == 200
