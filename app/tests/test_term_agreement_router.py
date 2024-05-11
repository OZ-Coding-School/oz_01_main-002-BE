from unittest.mock import patch

from fastapi import HTTPException
from tortoise.contrib.test import TestCase
from tortoise.exceptions import DoesNotExist

from app.dtos.terms_agreement_respones import TermsAgreementResponseOut
from app.models.terms import Terms
from app.models.users import User
from app.services.term_agreement_service import (
    service_create_terms_agreement,
    service_get_all_by_terms_agreement,
)


class TestTermAgreementRouter(TestCase):
    async def test_router_get_by_all_term_agreement(self) -> None:
        # given
        term = await Terms.create(
            id=1,
            name="이용약관",
            content="약관 내용",
            is_required=True,
            is_active=True,
        )
        user = await User.create(
            id=1,
            email="test@example.com",
            password="123",
            name="테스트",
            phone="01012341234",
            is_active=True,
            gender="male",
            age=20,
            nickname="닉네임",
            content="테스트 내용",
            is_verified=True,
            contact="0120312",
        )

        request_data = TermsAgreementResponseOut(
            user_id=user.id,
            term_id=term.id,
        )
        await service_create_terms_agreement(request_data)
        agreements = await service_get_all_by_terms_agreement()

        # then
        self.assertEqual(len(agreements), 1)
        self.assertEqual(agreements[0].user_id, request_data.user_id)
        self.assertEqual(agreements[0].term_id, request_data.term_id)

    async def test_router_create_term_agreement(self) -> None:
        term = await Terms.create(
            id=1,
            name="이용약관",
            content="약관 내용",
            is_required=True,
            is_active=True,
        )
        user = await User.create(
            id=1,
            email="test@example.com",
            password="123",
            name="테스트",
            phone="01012341234",
            is_active=True,
            gender="male",
            age=20,
            nickname="닉네임",
            content="테스트 내용",
            is_verified=True,
            contact="0120312",
        )
        # Terms.get_by_terms_id가 DoesNotExist 예외를 발생시키도록 모의 설정
        with patch("app.models.terms.Terms.get_by_terms_id", side_effect=DoesNotExist):
            request_data = TermsAgreementResponseOut(
                user_id=1,
                term_id=1,
            )

            with self.assertRaises(HTTPException) as context:
                await service_create_terms_agreement(request_data)

            # HTTPException의 상태 코드와 메세지를 확인
            self.assertEqual(context.exception.status_code, 404)
            self.assertIn("term 아이디 값이 없어여", context.exception.detail)

        with patch("app.models.users.User.get_by_user_id", side_effect=DoesNotExist):
            request_data = TermsAgreementResponseOut(
                user_id=1,
                term_id=1,
            )

            with self.assertRaises(HTTPException) as context:
                await service_create_terms_agreement(request_data)

            # HTTPException의 상태 코드와 메세지를 확인
            self.assertEqual(context.exception.status_code, 404)
            self.assertIn("user 아이디 값이 없어여", context.exception.detail)

        # when
        agreement = await service_create_terms_agreement(request_data)

        # then
        # 반환된 값이 예상 값과 일치하는지 확인
        self.assertIsInstance(agreement, TermsAgreementResponseOut)
        self.assertEqual(agreement.user_id, 1)
        self.assertEqual(agreement.term_id, 1)
