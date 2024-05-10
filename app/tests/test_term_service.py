from tortoise.contrib.test import TestCase

from app.dtos.terms_respones import TermsResponseOut
from app.models.terms import Terms
from app.services.term_service import service_create_term, service_get_all_by_terms


class TestArticleRouter(TestCase):
    async def test_create_term(self) -> None:
        # given
        request_data = TermsResponseOut(name="이용", content="약관")

        # when
        term = await service_create_term(request_data)

        # then
        self.assertEqual(term.name, "이용")
        self.assertEqual(term.content, "약관")

    async def test_get_all_terms(self) -> None:
        # given
        request_data = TermsResponseOut(name="이용", content="약관")
        request_data1 = TermsResponseOut(name="이용1", content="약관1")
        request_data2 = TermsResponseOut(name="이용2", content="약관2")
        request_data3 = TermsResponseOut(name="이용3", content="약관3")
        # 용어 추가
        await service_create_term(request_data)
        await service_create_term(request_data1)
        await service_create_term(request_data2)
        await service_create_term(request_data3)

        # when
        terms = await service_get_all_by_terms()

        # then
        # 용어가 세 개인지 확인
        self.assertEqual(len(terms), 4)
        # 각 용어의 속성 확인
        self.assertEqual(terms[0].name, "이용")
        self.assertEqual(terms[0].content, "약관")
        self.assertEqual(terms[0].is_required, True)
        self.assertEqual(terms[0].is_active, True)

        self.assertEqual(terms[1].name, "이용1")
        self.assertEqual(terms[1].content, "약관1")
        self.assertEqual(terms[1].is_required, True)
        self.assertEqual(terms[1].is_active, True)

        self.assertEqual(terms[2].name, "이용2")
        self.assertEqual(terms[2].content, "약관2")
        self.assertEqual(terms[2].is_required, True)
        self.assertEqual(terms[2].is_active, True)

        self.assertEqual(terms[3].name, "이용3")
        self.assertEqual(terms[3].content, "약관3")
        self.assertEqual(terms[3].is_required, True)
        self.assertEqual(terms[3].is_active, True)
