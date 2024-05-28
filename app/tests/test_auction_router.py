from datetime import datetime

from httpx import AsyncClient
from tortoise.contrib.test import TestCase

from app import app
from app.dtos.auction_response import AuctionCreate
from app.models.auctions import Auction
from app.models.categories import Category
from app.models.products import Product
from app.models.users import User


class TestAuctionRouter(TestCase):

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

    @staticmethod
    async def create_test_product() -> Product:
        return await Product.create(
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            modify=False,
            status="1",
            grade="상",
            category_id=1,
            user_id=1,
        )

    async def test_create_auction(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestAuctionRouter.create_test_user()
            test_category = await TestAuctionRouter.create_test_category()
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
            auction_data = AuctionCreate(
                product_id=product_data.id,
                charge=0,
                final_price=0,
                intstatus=True,
                end_time=datetime.now(),
            )
            response = await ac.post("/api/v1/auctions/", json=auction_data.dict())
            assert response.status_code == 200

    async def test_get_all_auctions(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestAuctionRouter.create_test_user()
            test_category = await TestAuctionRouter.create_test_category()
            product_data1 = await Product.create(
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
            product_data2 = await Product.create(
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
            auction_data1 = await Auction.create(
                product_id=product_data1.id, charge=0, status=True, end_time=datetime.now()
            )
            auction_data2 = await Auction.create(
                product_id=product_data2.id, charge=0, status=True, end_time=datetime.now()
            )

            response = await ac.get("/api/v1/auctions/")

            assert response.status_code == 200
            response_data = response.json()

            self.assertEqual(len(response_data), 2)

            assert response_data[0]["product_id"] == auction_data1.product_id
            assert response_data[0]["charge"] == auction_data1.charge

            assert response_data[1]["product_id"] == auction_data2.product_id
            assert response_data[1]["charge"] == auction_data2.charge

    async def test_get_auction_by_id(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestAuctionRouter.create_test_user()
            test_category = await TestAuctionRouter.create_test_category()
            product_data1 = await Product.create(
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
            auction_data1 = await Auction.create(
                product_id=product_data1.id, charge=0, status=True, end_time=datetime.now()
            )

            response = await ac.get(f"/api/v1/auctions/{auction_data1.id}")

            assert response.status_code == 200
            response_data = response.json()

            assert response_data["product_id"] == auction_data1.product_id
            assert response_data["charge"] == auction_data1.charge

    async def test_update_auction(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestAuctionRouter.create_test_user()
            test_category = await TestAuctionRouter.create_test_category()
            product_data1 = await Product.create(
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
            auction_data = await Auction.create(
                product_id=product_data1.id, charge=0, status=True, end_time=datetime.now()
            )

            update_auction_data = {
                "status": False,
                "is_active": "경매완료",
            }

            response = await ac.put(f"/api/v1/auctions/{auction_data.id}", json=update_auction_data)

            assert response.status_code == 200
            response_data = response.json()

            assert response_data["status"] == update_auction_data["status"]

    async def test_delete_auction(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            test_user = await TestAuctionRouter.create_test_user()
            test_category = await TestAuctionRouter.create_test_category()
            product_data1 = await Product.create(
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
            auction_data = await Auction.create(
                product_id=product_data1.id, charge=0, status=True, end_time=datetime.now()
            )

            response = await ac.delete(f"/api/v1/auctions/{auction_data.id}")

            assert response.status_code == 200
