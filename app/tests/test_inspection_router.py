# from tortoise.contrib.test import TestCase
#
# from app.dtos.inspection_response import (
#     InspectionCreateResponse,
#     InspectionUpdateResponse,
# )
# from app.models.inspections import Inspection
# from app.models.products import Product
# from app.models.users import User
# from app.services.inspection_service import (
#     service_create_inspection,
#     service_get_all_inspection,
#     service_get_detail_inspection,
#     service_get_one_inspection,
#     service_update_inspection,
# )
#
#
# class TestInspectionRouter(TestCase):
#     async def test_router_get_all_inspection(self) -> None:
#         test_user = await User.create_by_user(
#             name="test_user",
#             email="gudqls0516@naver.com",
#             password="pw12345",
#             gender="남",
#             age=12,
#             contact="test",
#             nickname="nick",
#             content="sdwdw",
#         )
#
#         # 제픔 2개 생성
#         product = await Product.create(
#             id=1,
#             name="테스트 제품",
#             content="테스트 내용",
#             bid_price=1,
#             duration=1,
#             status="1",
#             grade="상",
#             category="테스트 카테고리",
#             user_id=test_user.id,
#             modify=False,
#         )
#         product1 = await Product.create(
#             id=2,
#             name="테스트 제품",
#             content="테스트 내용",
#             bid_price=1,
#             duration=1,
#             status="1",
#             grade="상",
#             category="테스트 카테고리",
#             user_id=test_user.id,
#             modify=False,
#         )
#
#         # 검사 요청 데이터 생성
#         request_data = InspectionCreateResponse(inspector="유경록", product_id=product.id, inspection_count=1)
#         request_data1 = InspectionCreateResponse(inspector="로기", product_id=product1.id, inspection_count=1)
#
#         # 검사자 2개 생성
#         await service_create_inspection(request_data=request_data)
#         await service_create_inspection(request_data=request_data1)
#
#         inspections = await service_get_all_inspection()
#
#         # 검사자 2개인지 확인
#         self.assertEqual(len(inspections), 2)
#         # 각 검사자 확인
#         self.assertEqual(inspections[0].inspector, "유경록")
#         self.assertEqual(inspections[0].inspection_count, 1)
#         self.assertEqual(inspections[0].product_id, 1)
#
#         self.assertEqual(inspections[1].inspector, "로기")
#         self.assertEqual(inspections[1].inspection_count, 1)
#         self.assertEqual(inspections[1].product_id, 2)
#
#     async def test_router_get_one_inspection(self) -> None:
#         test_user = await User.create_by_user(
#             name="test_user",
#             email="gudqls0516@naver.com",
#             password="pw12345",
#             gender="남",
#             age=12,
#             contact="test",
#             nickname="nick",
#             content="sdwdw",
#         )
#         # 제품 생성
#         product = await Product.create(
#             id=1,
#             name="테스트 제품",
#             content="테스트 내용",
#             bid_price=1,
#             duration=1,
#             status="1",
#             grade="상",
#             category="테스트 카테고리",
#             user_id=test_user.id,
#             modify=False,
#         )
#
#         # 검사 생성
#         created_inspection = await Inspection.create(inspector="유경록", product_id=product.id, inspection_count=1)
#
#         # 제품 ID로 검사 조회
#         retrieved_inspection = await service_get_one_inspection(inspection_id=created_inspection.id)
#
#         # 생성된 검사와 조회된 검사가 일치하는지 확인
#         self.assertIsNotNone(retrieved_inspection)
#         self.assertEqual(retrieved_inspection.id, created_inspection.id)
#         self.assertEqual(retrieved_inspection.inspector, "유경록")
#         self.assertEqual(retrieved_inspection.product_id, product.id)
#         self.assertEqual(retrieved_inspection.inspection_count, 1)
#
#     async def test_router_get_detail_inspection(self) -> None:
#         test_user = await User.create_by_user(
#             name="test_user",
#             email="gudqls0516@naver.com",
#             password="pw12345",
#             gender="남",
#             age=12,
#             contact="test",
#             nickname="nick",
#             content="sdwdw",
#         )
#         # 제품 생성
#         product = await Product.create(
#             id=1,
#             name="테스트 제품",
#             content="테스트 내용",
#             bid_price=1,
#             duration=1,
#             status="1",
#             grade="상",
#             category="테스트 카테고리",
#             user_id=test_user.id,
#             modify=False,
#         )
#
#         # 검사 요청 데이터 생성
#         request_data = InspectionCreateResponse(inspector="유경록", product_id=product.id, inspection_count=1)
#
#         # 검사 생성
#         await service_create_inspection(request_data=request_data)
#
#         # 상세 검사 정보 가져오기
#         detail_inspections = await service_get_detail_inspection(product_id=product.id)
#
#         self.assertEqual(len(detail_inspections), 1)
#         self.assertEqual(detail_inspections[0].inspector, "유경록")
#         self.assertEqual(detail_inspections[0].inspection_count, 1)
#         self.assertEqual(detail_inspections[0].product_id, product.id)
#
#     async def test_router_create_inspection(self) -> None:
#
#         test_user = await User.create(
#             id=1,
#             name="test_user",
#             email="gudqls0516@naver.com",
#             password="pw12345",
#             gender="남",
#             age=12,
#             contact="test",
#             nickname="nick",
#             content="sdwdw",
#         )
#         # 제품 생성
#         product = await Product.create(
#             id=1,
#             name="테스트 제품",
#             content="테스트 내용",
#             bid_price=1,
#             duration=1,
#             status="1",
#             grade="상",
#             category="테스트 카테고리",
#             user_id=test_user.id,
#             modify=False,
#         )
#
#         # 검사 요청 데이터 생성
#         request_data = InspectionCreateResponse(inspector="유경록", product_id=product.id, inspection_count=3)
#
#         # 검사 생성
#         created_inspection = await service_create_inspection(request_data=request_data)
#
#         self.assertEqual(created_inspection.inspector, "유경록")
#         self.assertEqual(created_inspection.product_id, product.id)
#         self.assertEqual(created_inspection.inspection_count, 3)
#
#     async def test_router_update_inspection(self) -> None:
#
#         test_user = await User.create(
#             id=1,
#             name="test_user",
#             email="gudqls0516@naver.com",
#             password="pw12345",
#             gender="남",
#             age=12,
#             contact="test",
#             nickname="nick",
#             content="sdwdw",
#         )
#         # 제품 생성
#         product = await Product.create(
#             id=1,
#             name="테스트 제품",
#             content="테스트 내용",
#             bid_price=1,
#             duration=1,
#             status="1",
#             grade="상",
#             category="테스트 카테고리",
#             user_id=test_user.id,
#             modify=False,
#         )
#
#         # 검사 생성
#         created_inspection = await Inspection.create(inspector="유경록", product_id=product.id, inspection_count=3)
#
#         # 새로운 업데이트 요청 데이터 생성
#         updated_request_data = InspectionUpdateResponse(inspector="로기", inspection_count=2)
#
#         # 검사 업데이트
#         await service_update_inspection(inspection_id=created_inspection.id, request_data=updated_request_data)
#
#         # 업데이트된 검사 조회
#         updated_inspection = await Inspection.get_by_inspection_id(inspection_id=created_inspection.id)
#
#         self.assertEqual(updated_inspection.inspector, "로기")
#         self.assertEqual(updated_inspection.inspection_count, 2)
