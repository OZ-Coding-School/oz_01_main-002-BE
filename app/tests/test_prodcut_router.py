from tortoise.contrib.test import TestCase

from app.dtos.product_response import ProductCreate, ProductUpdate
from app.models.products import Product
from app.models.users import User
from app.services.product_service import (
    service_create_product,
    service_delete_product,
    service_get_all_products,
    service_get_by_product_id,
    service_update_product,
)


class TestProductRouter(TestCase):
    @staticmethod
    async def create_test_user() -> User:
        return await User.create_by_user(
            name="test_user",
            email="gudqls0516@naver.com",
            password="pw12345",
            gender="남",
            age=12,
            contact="test",
            nickname="nick",
            content="sdwdw",
        )

    async def test_create_product(self) -> None:
        test_user = await TestProductRouter.create_test_user()

        product_data = ProductCreate(
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            modify=False,
            status="1",
            grade="상",
            category="test category",
            user_id=test_user.id,
        )
        product = await service_create_product(product_data)

        self.assertEqual(product.name, product_data.name)
        self.assertEqual(product.content, product_data.content)
        self.assertEqual(product.bid_price, product_data.bid_price)
        self.assertEqual(product.duration, product_data.duration)
        self.assertEqual(product.status, product_data.status)
        self.assertEqual(product.grade, product_data.grade)
        self.assertEqual(product.category, product_data.category)

    async def test_get_all_products(self) -> None:
        test_user = await TestProductRouter.create_test_user()

        product_data1 = await Product.create(
            name="test_product1",
            content="test content",
            bid_price=1,
            duration=1,
            modify=False,
            status="1",
            grade="상",
            category="test category",
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
            category="test category",
            user_id=test_user.id,
        )
        product_data3 = await Product.create(
            name="test_product3",
            content="test content",
            bid_price=3,
            duration=3,
            modify=False,
            status="3",
            grade="하",
            category="test category",
            user_id=test_user.id,
        )
        product_data4 = await Product.create(
            name="test_product4",
            content="test content",
            bid_price=4,
            duration=4,
            modify=False,
            status="4",
            grade="상",
            category="test category",
            user_id=test_user.id,
        )

        products = await service_get_all_products()

        self.assertEqual(len(products), 4)

        self.assertEqual(products[0].id, product_data1.id)
        self.assertEqual(products[0].name, product_data1.name)
        self.assertEqual(products[0].content, product_data1.content)
        self.assertEqual(products[0].bid_price, product_data1.bid_price)
        self.assertEqual(products[0].duration, product_data1.duration)
        self.assertEqual(products[0].status, product_data1.status)
        self.assertEqual(products[0].grade, product_data1.grade)
        self.assertEqual(products[0].category, product_data1.category)

        self.assertEqual(products[1].id, product_data2.id)
        self.assertEqual(products[1].name, product_data2.name)
        self.assertEqual(products[1].content, product_data2.content)
        self.assertEqual(products[1].bid_price, product_data2.bid_price)
        self.assertEqual(products[1].duration, product_data2.duration)
        self.assertEqual(products[1].status, product_data2.status)
        self.assertEqual(products[1].grade, product_data2.grade)
        self.assertEqual(products[1].category, product_data2.category)

        self.assertEqual(products[2].id, product_data3.id)
        self.assertEqual(products[2].name, product_data3.name)
        self.assertEqual(products[2].content, product_data3.content)
        self.assertEqual(products[2].bid_price, product_data3.bid_price)
        self.assertEqual(products[2].duration, product_data3.duration)
        self.assertEqual(products[2].status, product_data3.status)
        self.assertEqual(products[2].grade, product_data3.grade)
        self.assertEqual(products[2].category, product_data3.category)

        self.assertEqual(products[3].id, product_data4.id)
        self.assertEqual(products[3].name, product_data4.name)
        self.assertEqual(products[3].content, product_data4.content)
        self.assertEqual(products[3].bid_price, product_data4.bid_price)
        self.assertEqual(products[3].duration, product_data4.duration)
        self.assertEqual(products[3].status, product_data4.status)
        self.assertEqual(products[3].grade, product_data4.grade)
        self.assertEqual(products[3].category, product_data4.category)

    async def test_get_product_id(self) -> None:
        test_user = await TestProductRouter.create_test_user()

        product_data1 = await Product.create(
            id=1,
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            modify=False,
            status="1",
            grade="상",
            category="test category",
            user_id=test_user.id,
        )

        product1 = await service_get_by_product_id(id=product_data1.id)

        self.assertEqual(product1.id, product_data1.id)
        self.assertEqual(product1.name, product_data1.name)
        self.assertEqual(product1.content, product_data1.content)
        self.assertEqual(product1.bid_price, product_data1.bid_price)
        self.assertEqual(product1.duration, product_data1.duration)
        self.assertEqual(product1.status, product_data1.status)
        self.assertEqual(product1.grade, product_data1.grade)
        self.assertEqual(product1.category, product_data1.category)

    async def test_update_product(self) -> None:
        test_user = await TestProductRouter.create_test_user()

        product_data1 = await Product.create(
            id=1,
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            modify=False,
            status="1",
            grade="상",
            category="test category",
            user_id=test_user.id,
        )

        product = await service_get_by_product_id(id=product_data1.id)

        update_product_data = ProductUpdate(
            name="new test product",
            content="new test content",
            bid_price=2,
            duration=2,
            status="2",
        )

        await service_update_product(id=product.id, product_data=update_product_data)

        update_product = await service_get_by_product_id(id=product_data1.id)
        self.assertEqual(update_product.name, "new test product")
        self.assertEqual(update_product.content, "new test content")
        self.assertEqual(update_product.bid_price, 2)
        self.assertEqual(update_product.duration, 2)
        self.assertEqual(update_product.status, "2")

    async def test_delete_product(self) -> None:
        test_user = await TestProductRouter.create_test_user()

        await Product.create(
            id=1,
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            modify=False,
            status="1",
            grade="상",
            category="test category",
            user_id=test_user.id,
        )
        await Product.create(
            id=2,
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            modify=False,
            status="1",
            grade="상",
            category="test category",
            user_id=test_user.id,
        )

        await service_delete_product(id=1)

        products = await service_get_all_products()

        self.assertEqual(len(products), 1)
