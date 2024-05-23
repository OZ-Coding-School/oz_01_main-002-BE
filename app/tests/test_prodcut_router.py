from httpx import AsyncClient
from tortoise.contrib.test import TestCase

from app import app
from app.dtos.product_response import ProductCreate
from app.models.categories import Category
from app.models.products import Product
from app.models.users import User


class TestProductRouter(TestCase):
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

    async def test_create_product(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestProductRouter.create_test_user()
            test_category = await TestProductRouter.create_test_category()
            product_data = ProductCreate(
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
            response = await ac.post("/api/v1/products/", json=product_data.dict())

            assert response.status_code == 200

    async def test_get_all_products(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestProductRouter.create_test_user()
            test_category = await TestProductRouter.create_test_category()

            product_data1 = await Product.create(
                name="test_product1",
                content="test content",
                bid_price=1,
                duration=1,
                modify=False,
                status="1",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )
            product_data2 = await Product.create(
                name="test_product2",
                content="test content",
                bid_price=2,
                duration=2,
                modify=False,
                status="2",
                grade="중",
                category_id=test_category.id,
                user_id=test_user.id,
            )

            response = await ac.get("/api/v1/products/")

            assert response.status_code == 200
            response_data = response.json()

            self.assertEqual(len(response_data), 2)

            assert response_data[0]["id"] == product_data1.id
            assert response_data[0]["name"] == product_data1.name
            assert response_data[0]["content"] == product_data1.content
            assert response_data[0]["bid_price"] == product_data1.bid_price
            assert response_data[0]["duration"] == product_data1.duration
            assert response_data[0]["status"] == product_data1.status
            assert response_data[0]["grade"] == product_data1.grade

            assert response_data[1]["id"] == product_data2.id
            assert response_data[1]["name"] == product_data2.name
            assert response_data[1]["content"] == product_data2.content
            assert response_data[1]["bid_price"] == product_data2.bid_price
            assert response_data[1]["duration"] == product_data2.duration
            assert response_data[1]["status"] == product_data2.status
            assert response_data[1]["grade"] == product_data2.grade

    async def test_get_product_id(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestProductRouter.create_test_user()
            test_category = await TestProductRouter.create_test_category()

            product_data = await Product.create(
                name="test_product1",
                content="test content",
                bid_price=1,
                duration=1,
                modify=False,
                status="1",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )

            response = await ac.get(f"/api/v1/products/{product_data.id}")

            assert response.status_code == 200
            response_data = response.json()

            assert response_data["id"] == product_data.id
            assert response_data["name"] == product_data.name
            assert response_data["content"] == product_data.content
            assert response_data["bid_price"] == product_data.bid_price
            assert response_data["duration"] == product_data.duration
            assert response_data["status"] == product_data.status
            assert response_data["grade"] == product_data.grade

    async def test_get_products_by_user_id(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestProductRouter.create_test_user()
            test_category = await TestProductRouter.create_test_category()

            product_data1 = await Product.create(
                name="test_product1",
                content="test content",
                bid_price=1,
                duration=1,
                modify=False,
                status="1",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )
            product_data2 = await Product.create(
                name="test_product2",
                content="test content",
                bid_price=2,
                duration=2,
                modify=False,
                status="2",
                grade="중",
                category_id=test_category.id,
                user_id=test_user.id,
            )

            response = await ac.get(f"/api/v1/products/user/{test_user.id}")

            assert response.status_code == 200
            response_data = response.json()

            assert len(response_data) == 2

            assert response_data[0]["id"] == product_data1.id
            assert response_data[0]["name"] == product_data1.name
            assert response_data[0]["content"] == product_data1.content
            assert response_data[0]["bid_price"] == product_data1.bid_price
            assert response_data[0]["duration"] == product_data1.duration
            assert response_data[0]["status"] == product_data1.status
            assert response_data[0]["grade"] == product_data1.grade

            assert response_data[1]["id"] == product_data2.id
            assert response_data[1]["name"] == product_data2.name
            assert response_data[1]["content"] == product_data2.content
            assert response_data[1]["bid_price"] == product_data2.bid_price
            assert response_data[1]["duration"] == product_data2.duration
            assert response_data[1]["status"] == product_data2.status
            assert response_data[1]["grade"] == product_data2.grade

    async def test_get_products_by_category_id(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestProductRouter.create_test_user()
            test_category = await TestProductRouter.create_test_category()

            product_data1 = await Product.create(
                name="test_product1",
                content="test content",
                bid_price=1,
                duration=1,
                modify=False,
                status="1",
                grade="상",
                category_id=test_category.id,
                user_id=test_user.id,
            )
            product_data2 = await Product.create(
                name="test_product2",
                content="test content",
                bid_price=2,
                duration=2,
                modify=False,
                status="2",
                grade="중",
                category_id=test_category.id,
                user_id=test_user.id,
            )

            response = await ac.get(f"/api/v1/products/categories/{test_category.id}")

            assert response.status_code == 200
            response_data = response.json()

            assert len(response_data) == 2

            assert response_data[0]["id"] == product_data1.id
            assert response_data[0]["name"] == product_data1.name
            assert response_data[0]["content"] == product_data1.content
            assert response_data[0]["bid_price"] == product_data1.bid_price
            assert response_data[0]["duration"] == product_data1.duration
            assert response_data[0]["status"] == product_data1.status
            assert response_data[0]["grade"] == product_data1.grade

            assert response_data[1]["id"] == product_data2.id
            assert response_data[1]["name"] == product_data2.name
            assert response_data[1]["content"] == product_data2.content
            assert response_data[1]["bid_price"] == product_data2.bid_price
            assert response_data[1]["duration"] == product_data2.duration
            assert response_data[1]["status"] == product_data2.status
            assert response_data[1]["grade"] == product_data2.grade

    async def test_update_product(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestProductRouter.create_test_user()
            test_category = await TestProductRouter.create_test_category()

            product_data = await Product.create(
                id=1,
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

            update_product_data = {
                "name": "new test product",
                "content": "new test content",
                "bid_price": 2,
                "duration": 2,
                "status": "2",
                "user_id": test_user.id,
                "category_id": test_category.id,
            }

            response = await ac.put(f"/api/v1/products/{product_data.id}", json=update_product_data)

            assert response.status_code == 200
            response_data = response.json()

            assert response_data["name"] == update_product_data["name"]
            assert response_data["content"] == update_product_data["content"]
            assert response_data["bid_price"] == update_product_data["bid_price"]
            assert response_data["duration"] == update_product_data["duration"]
            assert response_data["status"] == update_product_data["status"]

    async def test_delete_product(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestProductRouter.create_test_user()
            test_category = await TestProductRouter.create_test_category()

            product_data = await Product.create(
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

            response = await ac.delete(f"/api/v1/products/{product_data.id}")

            assert response.status_code == 200
