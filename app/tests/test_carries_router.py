from httpx import AsyncClient
from tortoise.contrib.test import TestCase

from app import app
from app.models.carries import Carries
from app.models.categories import Category
from app.models.products import Product
from app.models.users import User


class TestCarriesRouter(TestCase):
    @staticmethod
    async def create_test_user() -> User:
        return await User.create(
            name="test_user",
            email="gudqls0516@naver.com",
            password="pw12345",
            gender="남",
            age=12,
            contact="test",
            nickname="nick",
            content="sdwdw",
        )

    @staticmethod
    async def create_test_category() -> Category:
        return await Category.create(item_id=2, parent_id=2, sqe=2, name="나는 카테고리")

    @staticmethod
    async def create_test_product(category_id: int, user_id: int) -> Product:
        return await Product.create(
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            modify=False,
            status="1",
            grade="상",
            category_id=category_id,
            user_id=user_id,
        )

    async def test_router_create_carries(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # 테스트에 필요한 사용자 생성
            user_test = await self.create_test_user()
            category_test = await self.create_test_category()
            product_test = await self.create_test_product(user_id=user_test.id, category_id=category_test.id)

            # POST 요청에 사용될 데이터
            data = {
                "product_id": product_test.id,
                "address": "Test address",
                "sender": "Test sender",
                "contact": 1,
                "size": 1,
                "amount": 100,
            }

            # POST 요청을 보내고 응답을 받음
            response = await ac.post("/api/v1/carries/", json=data)

            # 응답 상태 코드 확인
            assert response.status_code == 201

    async def test_router_get_all_carries(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await self.create_test_user()
            category_test = await self.create_test_category()
            product_test = await self.create_test_product(user_id=user_test.id, category_id=category_test.id)
            await Carries.create(
                product_id=product_test.id,
                address="Test address",
                sender="Test sender",
                contact=1,
                size=1,
                amount=100,
            )
            await Carries.create(
                product_id=product_test.id,
                address="Test address1",
                sender="Test sender1",
                contact=2,
                size=2,
                amount=200,
            )
            # GET 요청을 보내고 응답을 받음
            response = await ac.get("/api/v1/carries/")

            # 응답 상태 코드 확인
            assert response.status_code == 200

            # 응답 데이터가 리스트인지 확인
            response_data = response.json()
            assert len(response_data) == 2

            # 응답 데이터의 내용 검증
            assert response_data[0]["address"] == "Test address"
            assert response_data[0]["sender"] == "Test sender"
            assert response_data[0]["contact"] == 1
            assert response_data[0]["size"] == 1
            assert response_data[0]["amount"] == 100

            assert response_data[1]["address"] == "Test address1"
            assert response_data[1]["sender"] == "Test sender1"
            assert response_data[1]["contact"] == 2
            assert response_data[1]["size"] == 2
            assert response_data[1]["amount"] == 200

    async def test_router_get_by_carries_id(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await self.create_test_user()
            category_test = await self.create_test_category()
            product_test = await self.create_test_product(user_id=user_test.id, category_id=category_test.id)
            carry_test = await Carries.create(
                product_id=product_test.id,
                address="Test address",
                sender="Test sender",
                contact=1,
                size=1,
                amount=100,
            )
            # GET 요청을 보내고 응답을 받음
            response = await ac.get(f"/api/v1/carries/{carry_test.id}")

            # 응답 상태 코드 확인
            assert response.status_code == 200

            # 응답 데이터 확인
            response_data = response.json()

            # 응답 데이터의 내용 검증
            assert response_data["address"] == "Test address"
            assert response_data["sender"] == "Test sender"
            assert response_data["contact"] == 1
            assert response_data["size"] == 1
            assert response_data["amount"] == 100

    async def test_router_update_carries(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await self.create_test_user()
            category_test = await self.create_test_category()
            product_test = await self.create_test_product(user_id=user_test.id, category_id=category_test.id)
            carry_test = await Carries.create(
                product_id=product_test.id,
                address="Test address",
                sender="Test sender",
                contact=1,
                size=1,
                amount=100,
            )
            # PUT 요청에 사용될 데이터
            data = {
                "address": "Updated address",
                "sender": "Updated sender",
                "contact": 1,
                "size": 1,
                "amount": 200,
            }

            # PUT 요청을 보내고 응답을 받음
            response = await ac.put(f"/api/v1/carries/{carry_test.id}", json=data)

            # 응답 상태 코드 확인
            assert response.status_code == 200

            # 업데이트된 carries 데이터 확인
            updated_carries = await Carries.get_or_none(address="Updated address")
            assert updated_carries is not None
            assert updated_carries.address == "Updated address"
            assert updated_carries.sender == "Updated sender"
            assert updated_carries.contact == 1
            assert updated_carries.size == 1
            assert updated_carries.amount == 200

    async def test_router_delete_carries(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await self.create_test_user()
            category_test = await self.create_test_category()
            product_test = await self.create_test_product(user_id=user_test.id, category_id=category_test.id)
            carry_test = await Carries.create(
                product_id=product_test.id,
                address="Test address",
                sender="Test sender",
                contact=1,
                size=1,
                amount=100,
            )
            # DELETE 요청을 보내고 응답을 받음
            response = await ac.delete(f"/api/v1/carries/{carry_test.id}")

            # 응답 상태 코드 확인
            assert response.status_code == 200

            # carries 데이터가 삭제되었는지 확인
            deleted_carries = await Carries.get_or_none(id=carry_test.id)
            assert deleted_carries is None
