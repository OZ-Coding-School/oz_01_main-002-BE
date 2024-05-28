from datetime import datetime
from typing import Any

from httpx import AsyncClient
from passlib.context import CryptContext  # type: ignore
from tortoise.contrib.test import TestCase

from app import app
from app.models.auctions import Auction
from app.models.categories import Category
from app.models.products import Product
from app.models.users import User
from app.models.winners import Winner

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestWinnerRouter(TestCase):
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

    @staticmethod
    async def create_test_auction(product_id: int) -> Auction:
        return await Auction.create(
            product_id=product_id,
            charge=0,
            status=True,
            end_time=datetime.now(),
        )

    async def test_service_get_by_winner(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # given
            user_test = await self.create_test_user()
            category_test = await self.create_test_category()
            product_test = await self.create_test_product(category_test.id, user_test.id)
            auction_test = await self.create_test_auction(product_test.id)

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}
            res = await ac.post("/api/v1/users/login", json=login_data)

            assert res.status_code == 200

            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            await Winner.create(
                product_id=product_test.id, auction_id=auction_test.id, user_id=user_test.id, bid_price=1000.0
            )
            response = await ac.get(f"/api/v1/winners/{product_test.id}", headers=headers)

            assert response.status_code == 200
            # then
            response_data = response.json()
            assert response_data["product_id"] == product_test.id
            assert response_data["auction_id"] == auction_test.id
            assert response_data["bid_price"] == 1000.0

    async def test_service_create_winner(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await self.create_test_user()
            category_test = await self.create_test_category()
            product_test = await self.create_test_product(category_test.id, user_test.id)
            auction_test = await self.create_test_auction(product_test.id)

            # 로그인하여 액세스 토큰을 획득합니다.
            login_data = {"email": "test@example.com", "password": "test_password"}
            res = await ac.post("/api/v1/users/login", json=login_data)

            assert res.status_code == 200

            token = res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}

            data = {
                "product_id": product_test.id,
                "user_id": user_test.id,
                "auction_id": auction_test.id,
                "bid_price": 1000.0,
            }
            response = await ac.post("/api/v1/winners/", json=data, headers=headers)
            assert response.status_code == 201
