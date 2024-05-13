from httpx import AsyncClient
from tortoise.contrib.test import TestCase

from app import app
from app.models.categories import Category


class TestCategoryRouter(TestCase):

    async def test_create_category(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("categories/", json={"item_id": 2, "parent_id": 0, "sqe": 2, "name": "카테고리"})
            response2 = await ac.post("categories/", json={"item_id": 2, "parent_id": 0, "sqe": 2, "name": "카테고리"})
        assert response.status_code == 201
        assert response2.status_code == 409

    async def test_get_all_categories(self) -> None:

        await Category.create(item_id=1, parent_id=0, sqe=1, name="나는 카테고리")
        await Category.create(item_id=1001, parent_id=1, sqe=1, name="나는 상의")
        await Category.create(item_id=1002, parent_id=1, sqe=2, name="나는 하의")
        await Category.create(item_id=1003, parent_id=1, sqe=3, name="나는 신발")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("categories/")

        assert response.status_code == 200

        assert response.json()[0]["item_id"] == 1
        assert response.json()[0]["parent_id"] == 0
        assert response.json()[0]["sqe"] == 1
        assert response.json()[0]["name"] == "나는 카테고리"

        assert response.json()[1]["item_id"] == 1001
        assert response.json()[1]["parent_id"] == 1
        assert response.json()[1]["sqe"] == 1
        assert response.json()[1]["name"] == "나는 상의"

        assert response.json()[2]["item_id"] == 1002
        assert response.json()[2]["parent_id"] == 1
        assert response.json()[2]["sqe"] == 2
        assert response.json()[2]["name"] == "나는 하의"

        assert response.json()[3]["item_id"] == 1003
        assert response.json()[3]["parent_id"] == 1
        assert response.json()[3]["sqe"] == 3
        assert response.json()[3]["name"] == "나는 신발"

    async def test_get_category_by_item_id(self) -> None:

        await Category.create(item_id=1, parent_id=0, sqe=1, name="이것은 카테고리")
        await Category.create(item_id=1001, parent_id=1, sqe=1, name="이것은 상의")
        await Category.create(item_id=1002, parent_id=1, sqe=2, name="이것은 하의")
        await Category.create(item_id=1003, parent_id=1, sqe=3, name="이것은 신발")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("categories/1")
            response2 = await ac.get("categories/1001")
            response3 = await ac.get("categories/1002")
            response4 = await ac.get("categories/1003")

        assert response.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200

        assert response.json()["item_id"] == 1
        assert response.json()["parent_id"] == 0
        assert response.json()["sqe"] == 1
        assert response.json()["name"] == "이것은 카테고리"

        assert response2.json()["item_id"] == 1001
        assert response2.json()["parent_id"] == 1
        assert response2.json()["sqe"] == 1
        assert response2.json()["name"] == "이것은 상의"

        assert response3.json()["item_id"] == 1002
        assert response3.json()["parent_id"] == 1
        assert response3.json()["sqe"] == 2
        assert response3.json()["name"] == "이것은 하의"

        assert response4.json()["item_id"] == 1003
        assert response4.json()["parent_id"] == 1
        assert response4.json()["sqe"] == 3
        assert response4.json()["name"] == "이것은 신발"

    async def test_get_category_children(self) -> None:

        await Category.create(item_id=1, parent_id=0, sqe=1, name="카테고리")

        await Category.create(item_id=1001, parent_id=1, sqe=1, name="상의")
        await Category.create(item_id=1002, parent_id=1, sqe=2, name="하의")
        await Category.create(item_id=1003, parent_id=1, sqe=3, name="신발")

        await Category.create(item_id=2001, parent_id=1001, sqe=1, name="후드")
        await Category.create(item_id=2002, parent_id=1001, sqe=2, name="셔츠")
        await Category.create(item_id=2003, parent_id=1001, sqe=3, name="맨투맨")

        await Category.create(item_id=2004, parent_id=1002, sqe=1, name="치마")
        await Category.create(item_id=2005, parent_id=1002, sqe=2, name="바지")

        await Category.create(item_id=2007, parent_id=1003, sqe=1, name="나이키")
        await Category.create(item_id=2008, parent_id=1003, sqe=2, name="아디다스")
        await Category.create(item_id=2009, parent_id=1003, sqe=3, name="컨버스")

        await Category.create(item_id=3001, parent_id=2007, sqe=1, name="에어맥스")
        await Category.create(item_id=3002, parent_id=2007, sqe=2, name="에어조던")
        await Category.create(item_id=3003, parent_id=2007, sqe=3, name="에어포스")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response1 = await ac.get("categories/parent_id/0")
            response2 = await ac.get("categories/parent_id/1")
            response3 = await ac.get("categories/parent_id/1001")
            response4 = await ac.get("categories/parent_id/1002")
            response5 = await ac.get("categories/parent_id/1003")
            response6 = await ac.get("categories/parent_id/2007")
            response7 = await ac.get("categories/parent_id/2008")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert response5.status_code == 200
        assert response6.status_code == 200
        assert response7.status_code == 404

        assert response1.json()[0]["item_id"] == 1
        assert response1.json()[0]["parent_id"] == 0
        assert response1.json()[0]["sqe"] == 1
        assert response1.json()[0]["name"] == "카테고리"

        assert response2.json()[0]["item_id"] == 1001
        assert response2.json()[0]["parent_id"] == 1
        assert response2.json()[0]["sqe"] == 1
        assert response2.json()[0]["name"] == "상의"

        assert response2.json()[1]["item_id"] == 1002
        assert response2.json()[1]["parent_id"] == 1
        assert response2.json()[1]["sqe"] == 2
        assert response2.json()[1]["name"] == "하의"

        assert response2.json()[2]["item_id"] == 1003
        assert response2.json()[2]["parent_id"] == 1
        assert response2.json()[2]["sqe"] == 3
        assert response2.json()[2]["name"] == "신발"

        assert response3.json()[0]["item_id"] == 2001
        assert response3.json()[0]["parent_id"] == 1001
        assert response3.json()[0]["sqe"] == 1
        assert response3.json()[0]["name"] == "후드"

        assert response3.json()[1]["item_id"] == 2002
        assert response3.json()[1]["parent_id"] == 1001
        assert response3.json()[1]["sqe"] == 2
        assert response3.json()[1]["name"] == "셔츠"

        assert response3.json()[2]["item_id"] == 2003
        assert response3.json()[2]["parent_id"] == 1001
        assert response3.json()[2]["sqe"] == 3
        assert response3.json()[2]["name"] == "맨투맨"

        assert response4.json()[0]["item_id"] == 2004
        assert response4.json()[0]["parent_id"] == 1002
        assert response4.json()[0]["sqe"] == 1
        assert response4.json()[0]["name"] == "치마"

        assert response4.json()[1]["item_id"] == 2005
        assert response4.json()[1]["parent_id"] == 1002
        assert response4.json()[1]["sqe"] == 2
        assert response4.json()[1]["name"] == "바지"

        assert response5.json()[0]["item_id"] == 2007
        assert response5.json()[0]["parent_id"] == 1003
        assert response5.json()[0]["sqe"] == 1
        assert response5.json()[0]["name"] == "나이키"

        assert response5.json()[1]["item_id"] == 2008
        assert response5.json()[1]["parent_id"] == 1003
        assert response5.json()[1]["sqe"] == 2
        assert response5.json()[1]["name"] == "아디다스"

        assert response5.json()[2]["item_id"] == 2009
        assert response5.json()[2]["parent_id"] == 1003
        assert response5.json()[2]["sqe"] == 3
        assert response5.json()[2]["name"] == "컨버스"

        assert response6.json()[0]["item_id"] == 3001
        assert response6.json()[0]["parent_id"] == 2007
        assert response6.json()[0]["sqe"] == 1
        assert response6.json()[0]["name"] == "에어맥스"

        assert response6.json()[1]["item_id"] == 3002
        assert response6.json()[1]["parent_id"] == 2007
        assert response6.json()[1]["sqe"] == 2
        assert response6.json()[1]["name"] == "에어조던"

        assert response6.json()[2]["item_id"] == 3003
        assert response6.json()[2]["parent_id"] == 2007
        assert response6.json()[2]["sqe"] == 3
        assert response6.json()[2]["name"] == "에어포스"

    async def test_delete_category(self) -> None:

        await Category.create(item_id=10001, parent_id=0, sqe=1, name="카테고리1")
        await Category.create(item_id=20002, parent_id=0, sqe=2, name="카테고리2")

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete("categories/10001")
            response1 = await ac.get("categories/10001")
            response2 = await ac.get("categories/20002")
            response3 = await ac.get("categories/")

            assert response.status_code == 200
            assert response1.status_code == 404
            assert response2.status_code == 200
            assert response3.json()[0]["item_id"] == 20002
