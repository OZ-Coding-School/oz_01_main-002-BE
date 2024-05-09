from tortoise.contrib.test import TestCase

from app.services.product_service import (
    service_create_product,
    service_get_all_products,
)


class TestProductRouter(TestCase):
    async def test_create_product(self) -> None:
        product_id = 1
        product = await service_create_product(
            id=product_id,
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            status="1",
            grade="상",
            category="test category",
        )

        self.assertEqual(product.id, product_id)
        self.assertEqual(product.name, "test_product")
        self.assertEqual(product.content, "test content")
        self.assertEqual(product.bid_price, 1)
        self.assertEqual(product.duration, 1)
        self.assertEqual(product.status, "1")
        self.assertEqual(product.grade, "상")
        self.assertEqual(product.category, "test category")

    async def test_get_all_products(self) -> None:
        await service_create_product(
            id=1,
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            status="1",
            grade="상",
            category="test category",
        )
        await service_create_product(
            id=2,
            name="test_product",
            content="test content",
            bid_price=2,
            duration=2,
            status="2",
            grade="상",
            category="test category",
        )
        await service_create_product(
            id=3,
            name="test_product",
            content="test content",
            bid_price=3,
            duration=3,
            status="3",
            grade="상",
            category="test category",
        )
        await service_create_product(
            id=4,
            name="test_product",
            content="test content",
            bid_price=4,
            duration=4,
            status="4",
            grade="상",
            category="test category",
        )
        products = await service_get_all_products()

        self.assertEqual(len(products), 4)

        self.assertEqual(products[0].id, 1)
        self.assertEqual(products[0].name, "test_product")
        self.assertEqual(products[0].content, "test content")
        self.assertEqual(products[0].bid_price, 1)
        self.assertEqual(products[0].duration, 1)
        self.assertEqual(products[0].status, "1")
        self.assertEqual(products[0].grade, "상")
        self.assertEqual(products[0].category, "test category")

        self.assertEqual(products[1].id, 2)
        self.assertEqual(products[1].name, "test_product")
        self.assertEqual(products[1].content, "test content")
        self.assertEqual(products[1].bid_price, 2)
        self.assertEqual(products[1].duration, 2)
        self.assertEqual(products[1].status, "2")
        self.assertEqual(products[1].grade, "상")
        self.assertEqual(products[1].category, "test category")

        self.assertEqual(products[2].id, 3)
        self.assertEqual(products[2].name, "test_product")
        self.assertEqual(products[2].content, "test content")
        self.assertEqual(products[2].bid_price, 3)
        self.assertEqual(products[2].duration, 3)
        self.assertEqual(products[2].status, "3")
        self.assertEqual(products[2].grade, "상")
        self.assertEqual(products[2].category, "test category")

        self.assertEqual(products[3].id, 4)
        self.assertEqual(products[3].name, "test_product")
        self.assertEqual(products[3].content, "test content")
        self.assertEqual(products[3].bid_price, 4)
        self.assertEqual(products[3].duration, 4)
        self.assertEqual(products[3].status, "4")
        self.assertEqual(products[3].grade, "상")
        self.assertEqual(products[3].category, "test category")
