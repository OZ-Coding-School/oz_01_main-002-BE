from tortoise.contrib.test import TestCase

from app.dtos.category_response import CategoryBaseResponse
from app.services.category_service import (
    service_create_category,
    service_delete_category,
    service_get_all_categories,
    service_get_categories_children,
    service_get_category_by_item_id,
)


class TestCategoryRouter(TestCase):

    async def test_create_category(self) -> None:
        category = await service_create_category(CategoryBaseResponse(item_id=1, parent_id=0, sqe=1, name="카테고리"))
        self.assertEqual(category.item_id, 1)
        self.assertEqual(category.parent_id, 0)
        self.assertEqual(category.sqe, 1)
        self.assertEqual(category.name, "카테고리")

    async def test_get_all_categories(self) -> None:

        await service_create_category(CategoryBaseResponse(item_id=1, parent_id=0, sqe=1, name="나는 카테고리"))
        await service_create_category(CategoryBaseResponse(item_id=1001, parent_id=1, sqe=1, name="나는 상의"))
        await service_create_category(CategoryBaseResponse(item_id=1002, parent_id=1, sqe=2, name="나는 하의"))
        await service_create_category(CategoryBaseResponse(item_id=1003, parent_id=1, sqe=3, name="나는 신발"))

        categories = await service_get_all_categories()

        self.assertEqual(categories[0].item_id, 1)
        self.assertEqual(categories[0].parent_id, 0)
        self.assertEqual(categories[0].sqe, 1)
        self.assertEqual(categories[0].name, "나는 카테고리")

        self.assertEqual(categories[1].item_id, 1001)
        self.assertEqual(categories[1].parent_id, 1)
        self.assertEqual(categories[1].sqe, 1)
        self.assertEqual(categories[1].name, "나는 상의")

        self.assertEqual(categories[2].item_id, 1002)
        self.assertEqual(categories[2].parent_id, 1)
        self.assertEqual(categories[2].sqe, 2)
        self.assertEqual(categories[2].name, "나는 하의")

        self.assertEqual(categories[3].item_id, 1003)
        self.assertEqual(categories[3].parent_id, 1)
        self.assertEqual(categories[3].sqe, 3)
        self.assertEqual(categories[3].name, "나는 신발")

    async def test_get_category_by_item_id(self) -> None:

        await service_create_category(CategoryBaseResponse(item_id=1, parent_id=0, sqe=1, name="이것은 카테고리"))
        await service_create_category(CategoryBaseResponse(item_id=1001, parent_id=1, sqe=1, name="이것은 상의"))
        await service_create_category(CategoryBaseResponse(item_id=1002, parent_id=1, sqe=2, name="이것은 하의"))
        await service_create_category(CategoryBaseResponse(item_id=1003, parent_id=1, sqe=3, name="이것은 신발"))

        category1 = await service_get_category_by_item_id(1)
        category2 = await service_get_category_by_item_id(1001)
        category3 = await service_get_category_by_item_id(1002)
        category4 = await service_get_category_by_item_id(1003)

        self.assertEqual(category1.item_id, 1)
        self.assertEqual(category1.parent_id, 0)
        self.assertEqual(category1.sqe, 1)
        self.assertEqual(category1.name, "이것은 카테고리")

        self.assertEqual(category2.item_id, 1001)
        self.assertEqual(category2.parent_id, 1)
        self.assertEqual(category2.sqe, 1)
        self.assertEqual(category2.name, "이것은 상의")

        self.assertEqual(category3.item_id, 1002)
        self.assertEqual(category3.parent_id, 1)
        self.assertEqual(category3.sqe, 2)
        self.assertEqual(category3.name, "이것은 하의")

        self.assertEqual(category4.item_id, 1003)
        self.assertEqual(category4.parent_id, 1)
        self.assertEqual(category4.sqe, 3)
        self.assertEqual(category4.name, "이것은 신발")

    async def test_get_category_children(self) -> None:

        await service_create_category(CategoryBaseResponse(item_id=1, parent_id=0, sqe=1, name="카테고리"))
        await service_create_category(CategoryBaseResponse(item_id=1001, parent_id=1, sqe=1, name="상의"))
        await service_create_category(CategoryBaseResponse(item_id=1002, parent_id=1, sqe=2, name="하의"))
        await service_create_category(CategoryBaseResponse(item_id=1003, parent_id=1, sqe=3, name="신발"))
        await service_create_category(CategoryBaseResponse(item_id=2001, parent_id=1001, sqe=1, name="후드"))
        await service_create_category(CategoryBaseResponse(item_id=2002, parent_id=1001, sqe=2, name="셔츠"))
        await service_create_category(CategoryBaseResponse(item_id=2003, parent_id=1001, sqe=3, name="맨투맨"))
        await service_create_category(CategoryBaseResponse(item_id=2004, parent_id=1002, sqe=1, name="치마"))
        await service_create_category(CategoryBaseResponse(item_id=2005, parent_id=1002, sqe=2, name="바지"))
        await service_create_category(CategoryBaseResponse(item_id=2006, parent_id=1002, sqe=3, name="치마바지"))
        await service_create_category(CategoryBaseResponse(item_id=2007, parent_id=1003, sqe=1, name="나이키"))
        await service_create_category(CategoryBaseResponse(item_id=2008, parent_id=1003, sqe=2, name="아디다스"))
        await service_create_category(CategoryBaseResponse(item_id=2009, parent_id=1003, sqe=3, name="컨버스"))
        await service_create_category(CategoryBaseResponse(item_id=3001, parent_id=2007, sqe=1, name="에어맥스"))
        await service_create_category(CategoryBaseResponse(item_id=3002, parent_id=2007, sqe=2, name="에어조던"))
        await service_create_category(CategoryBaseResponse(item_id=3003, parent_id=2007, sqe=3, name="에어포스"))

        main_categories = await service_get_categories_children(1)

        self.assertEqual(main_categories[0].name, "상의")
        self.assertEqual(main_categories[1].name, "하의")
        self.assertEqual(main_categories[2].name, "신발")

        second_categories1 = await service_get_categories_children(1001)

        self.assertEqual(second_categories1[0].name, "후드")
        self.assertEqual(second_categories1[1].name, "셔츠")
        self.assertEqual(second_categories1[2].name, "맨투맨")

        second_categories2 = await service_get_categories_children(1002)

        self.assertEqual(second_categories2[0].name, "치마")
        self.assertEqual(second_categories2[1].name, "바지")
        self.assertEqual(second_categories2[2].name, "치마바지")

        second_categories3 = await service_get_categories_children(1003)

        self.assertEqual(second_categories3[0].name, "나이키")
        self.assertEqual(second_categories3[1].name, "아디다스")
        self.assertEqual(second_categories3[2].name, "컨버스")

        third_categories = await service_get_categories_children(2007)

        self.assertEqual(third_categories[0].name, "에어맥스")
        self.assertEqual(third_categories[1].name, "에어조던")
        self.assertEqual(third_categories[2].name, "에어포스")

    async def test_delete_category(self) -> None:

        await service_create_category(CategoryBaseResponse(item_id=10001, parent_id=0, sqe=1, name="카테고리1"))
        await service_create_category(CategoryBaseResponse(item_id=20002, parent_id=0, sqe=2, name="카테고리2"))

        await service_delete_category(20002)

        categories = await service_get_all_categories()

        self.assertEqual(len(categories), 1)
