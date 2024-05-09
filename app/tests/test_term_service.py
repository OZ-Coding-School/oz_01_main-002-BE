from tortoise.contrib.test import TestCase

from app.models.terms import Terms
from app.services.term_service import service_create_term, service_get_all_terms


class TestArticleRouter(TestCase):
    async def test_create_term(self) -> None:
        # given
        term_id = "1"

        # when
        term = await service_create_term(id=term_id, name="유경록", content="이용약관")

        # then
        self.assertEqual(term.id, term_id)
        self.assertEqual(term.name, "유경록")
        self.assertEqual(term.content, "이용약관")
        self.assertEqual(term.is_required, True)
        self.assertEqual(term.is_active, True)

    async def test_get_all_terms(self) -> None:
        # given
        # 용어 추가
        await service_create_term(id="1", name="유경록", content="이용약관1")
        await service_create_term(id="2", name="유경록", content="이용약관2")
        await service_create_term(id="3", name="유경록", content="이용약관3")
        await service_create_term(id="4", name="유경록", content="이용약관4")

        # when
        terms = await service_get_all_terms()

        # then
        # 용어가 세 개인지 확인
        self.assertEqual(len(terms), 4)
        # 각 용어의 속성 확인
        self.assertEqual(terms[0].id, "1")
        self.assertEqual(terms[0].name, "유경록")
        self.assertEqual(terms[0].content, "이용약관1")
        self.assertEqual(terms[0].is_required, True)
        self.assertEqual(terms[0].is_active, True)

        self.assertEqual(terms[1].id, "2")
        self.assertEqual(terms[1].name, "유경록")
        self.assertEqual(terms[1].content, "이용약관2")
        self.assertEqual(terms[1].is_required, True)
        self.assertEqual(terms[1].is_active, True)

        self.assertEqual(terms[2].id, "3")
        self.assertEqual(terms[2].name, "유경록")
        self.assertEqual(terms[2].content, "이용약관3")
        self.assertEqual(terms[2].is_required, True)
        self.assertEqual(terms[2].is_active, True)

        self.assertEqual(terms[3].id, "4")
        self.assertEqual(terms[3].name, "유경록")
        self.assertEqual(terms[3].content, "이용약관4")
        self.assertEqual(terms[3].is_required, True)
        self.assertEqual(terms[3].is_active, True)
