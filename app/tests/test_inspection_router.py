from httpx import AsyncClient
from tortoise.contrib.test import TestCase

from app import app
from app.models.categories import Category
from app.models.inspections import Inspection
from app.models.products import Product
from app.models.users import User


class TestInspectionRouter(TestCase):
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
        return await Category.create(item_id=1, parent_id=1, sqe=1, name="나는 카테고리")

    async def test_router_get_all_inspection(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await self.create_test_user()
            test_category = await self.create_test_category()
            product_test = await Product.create(
                name="test_product",
                content="test content",
                bid_price=1,
                duration=1,
                modify=False,
                status="1",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )
            product_test1 = await Product.create(
                name="test_product1",
                content="test content1",
                bid_price=11,
                duration=11,
                modify=False,
                status="11",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )
            # Inspection 데이터 생성
            await Inspection.create(inspector="inspector1", product_id=product_test.id, inspection_count=1)
            await Inspection.create(inspector="inspector2", product_id=product_test1.id, inspection_count=2)

            # GET 요청을 보내고 응답을 받음
            response = await ac.get("/api/v1/inspection/")

            # 응답 상태 코드 확인
            assert response.status_code == 200

            # 응답 데이터 확인
            response_data = response.json()
            assert len(response_data) == 2

            # 응답 데이터의 내용 검증
            assert response_data[0]["inspector"] == "inspector1"
            assert response_data[0]["product_id"] == product_test.id
            assert response_data[0]["inspection_count"] == 1

            assert response_data[1]["inspector"] == "inspector2"
            assert response_data[1]["product_id"] == product_test1.id
            assert response_data[1]["inspection_count"] == 2

    # Test case for creating an inspection
    async def test_router_create_inspection(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await self.create_test_user()
            test_category = await self.create_test_category()
            # Product 데이터 생성
            product_test = await Product.create(
                name="test_product",
                content="test content",
                bid_price=1,
                duration=1,
                modify=False,
                status="1",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )

            # POST 요청에 사용될 데이터
            data = {"product_id": product_test.id, "inspector": "inspector1", "inspection_count": 1}

            # POST 요청을 보내고 응답을 받음
            response = await ac.post("/api/v1/inspection/", json=data)

            # 응답 상태 코드 확인
            assert response.status_code == 200

            # Inspection 데이터가 생성되었는지 확인
            inspection = await Inspection.get_or_none(product_id=product_test.id)
            assert inspection is not None
            assert inspection.inspector == "inspector1"
            assert inspection.product_id == product_test.id
            assert inspection.inspection_count == 1

    async def test_router_get_detail_inspection(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await self.create_test_user()
            test_category = await self.create_test_category()
            product_test = await Product.create(
                name="test_product",
                content="test content",
                bid_price=1,
                duration=1,
                modify=False,
                status="1",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )
            # Inspection 데이터 생성
            await Inspection.create(inspector="inspector1", product_id=product_test.id, inspection_count=1)

            # GET 요청을 보내고 응답을 받음
            response = await ac.get(f"/api/v1/inspection/product/{product_test.id}")

            # 응답 상태 코드 확인
            assert response.status_code == 200

            # 응답 데이터 확인
            response_data = response.json()
            assert len(response_data) == 1

            # 응답 데이터의 내용 검증
            assert response_data[0]["inspector"] == "inspector1"
            assert response_data[0]["product_id"] == product_test.id
            assert response_data[0]["inspection_count"] == 1

    async def test_router_get_one_inspection(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await self.create_test_user()
            test_category = await self.create_test_category()
            product_test = await Product.create(
                name="test_product",
                content="test content",
                bid_price=1,
                duration=1,
                modify=False,
                status="1",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )
            # Inspection 데이터 생성
            await Inspection.create(inspector="inspector1", product_id=product_test.id, inspection_count=1)

            # GET 요청을 보내고 응답을 받음
            response = await ac.get(f"/api/v1/inspection/{product_test.id}")

            # 응답 상태 코드 확인
            assert response.status_code == 200

            # 응답 데이터 확인
            response_data = response.json()

            # 응답 데이터의 내용 검증
            assert response_data["inspector"] == "inspector1"
            assert response_data["product_id"] == product_test.id
            assert response_data["inspection_count"] == 1

    async def test_router_update_inspection(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await self.create_test_user()
            test_category = await self.create_test_category()
            product_test = await Product.create(
                name="test_product",
                content="test content",
                bid_price=1,
                duration=1,
                modify=False,
                status="1",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )
            # Inspection 데이터 생성
            await Inspection.create(inspector="inspector1", product_id=product_test.id, inspection_count=1)

            # PUT 요청에 사용될 데이터
            data = {"inspector": "updated_inspector", "inspection_count": 2}

            # PUT 요청을 보내고 응답을 받음
            response = await ac.put(f"/api/v1/inspection/{product_test.id}", json=data)

            # 응답 상태 코드 확인
            assert response.status_code == 200
