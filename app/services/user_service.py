import logging
import random
import re
import smtplib
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import orjson
from fastapi import Depends, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # type: ignore
from tortoise.exceptions import DoesNotExist, IntegrityError, ValidationError

from app.configs import settings
from app.dtos.image_response import ImageResponse
from app.dtos.terms_agreement_response import TermsAgreementCreateResponse
from app.dtos.terms_response import TermIDResponse
from app.dtos.user_response import (
    SendVerificationCodeResponse,
    UserCoinCreateResponse,
    UserGetProfileResponse,
    UserLoginResponse,
    UserSignUpResponse,
    UserUpdateProfileResponse,
    VerifyContactResponse,
    VerifyEmailResponse,
    VerifyNicknameResponse,
)
from app.models.address import Address
from app.models.images import Image
from app.models.users import User
from app.services.image_service import service_get_images, service_upload_image
from app.services.term_agreement_service import service_create_terms_agreement
from app.utils.redis_ import redis

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def is_valid_contact(contact: str) -> bool:
    pattern = r"^01[0-9]-\d{4}-\d{4}$"
    return re.match(pattern, contact) is not None


def generate_verification_code() -> int:
    return int("".join(str(random.randint(0, 9)) for _ in range(6)))


async def send_verification_email(request_data: SendVerificationCodeResponse) -> dict[str, str]:
    try:
        if not is_valid_email(request_data.email):
            raise HTTPException(status_code=400, detail="Invalid email")

        user = await User.get(email=request_data.email)

        if user.email == request_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    except DoesNotExist:
        pass

    try:
        verification_code = generate_verification_code()
        email_content = f"""
        안녕하세요 우리동네 경매장 입니다!
        
        본 이메일은 자사 서비스를 사용하기 위한 필수 사항입니다.
        
        아래의 코드는 절대 타인에게 노출되지 않도록 주의 바랍니다.
        
        코드입력과 함께 회원가입 절차를 완료하여 주시기 바랍니다.
        
        인증코드 : {verification_code}
        
        감사합니다.
        
        우리동네 경매장
        """
        msg = MIMEMultipart()
        msg["From"] = settings.GMAIL_USERNAME
        msg["To"] = request_data.email
        msg["Subject"] = "우리동네 경매장 이메일 인증코드"

        msg.attach(MIMEText(email_content, "plain"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(settings.GMAIL_USERNAME, settings.GMAIL_PASSWORD)

        result = await redis.get(request_data.email)

        if result is None:
            await redis.set(
                request_data.email, orjson.dumps({"email": request_data.email, "code": str(verification_code)})
            )
            await redis.expire(request_data.email, 60)
        else:
            code = orjson.loads(result)["code"]

            if len(code) == 6:
                await redis.delete(request_data.email)
                await redis.set(
                    request_data.email, orjson.dumps({"email": request_data.email, "code": str(verification_code)})
                )
                await redis.expire(request_data.email, 60)

        server.sendmail(settings.GMAIL_USERNAME, request_data.email, msg.as_string())
        server.close()

        return {"message": "Successfully sent the verification code to user email"}

    except Exception as e:
        logging.error(f"An error occurred while sending verification email: {e}")
        return {"error": str(e)}


async def service_code_authentication(request_data: VerifyEmailResponse) -> dict[str, str]:
    try:
        email = await redis.get(request_data.email)
        if email is None:
            raise HTTPException(status_code=400, detail="Bad Request - Incorrect Email")

        elif request_data.email == orjson.loads(email)["email"]:
            if str(request_data.code) == orjson.loads(await redis.get(request_data.email))["code"]:
                await redis.delete(request_data.email)
                return {"message": "Clear"}
        raise HTTPException(status_code=400, detail="Bad Request - Incorrect Code")

    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Bad Request - Check user email as the authentication email ")


async def service_nickname_verification(request_data: VerifyNicknameResponse) -> dict[str, str]:
    if request_data.nickname.isdigit():
        raise HTTPException(status_code=400, detail="Bad Request - Nickname must string")

    try:
        user = await User.get_by_user_nickname(nickname=request_data.nickname)
        if user.nickname == request_data.nickname:
            raise HTTPException(status_code=400, detail="Bad Request - Nickname already registered")

        return {"message": "OK - Nickname available"}

    except DoesNotExist:
        return {"message": "OK - Nickname available"}


async def service_contact_verification(request_data: VerifyContactResponse) -> dict[str, str]:
    try:
        if not is_valid_contact(request_data.contact):
            raise HTTPException(status_code=400, detail="Bad Request - Invalid Contact")

        user = await User.get_by_user_contact(contact=request_data.contact)

        if user.contact == request_data.contact:
            raise HTTPException(status_code=400, detail="Bad Request - Contact already registered")
        return {"message": "OK - Contact available"}

    except DoesNotExist:
        return {"message": "OK - Contact available"}


async def service_signup(request_data: UserSignUpResponse, term_data: list[TermIDResponse]) -> dict[str, str]:
    try:
        await User.get(email=request_data.email)
        raise HTTPException(status_code=400, detail="Bad Request - User already registered")

    except DoesNotExist:
        pass

    try:
        await User.create_by_user(request_data)

        user = await User.get(email=request_data.email)

        data = [term.id for term in term_data]

        user_term_agreements = [TermsAgreementCreateResponse(user_id=user.id, term_id=term_id) for term_id in data]

        for user_term_agreement in user_term_agreements:
            await service_create_terms_agreement(user_term_agreement, user.id)

        return {"message": "Created - successfully signup!"}

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Bad Request - User already registered")


def create_access_token(data: Mapping[str, str | float], expires_delta: timedelta | None = None) -> Any:
    to_encode = dict(data)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    to_encode.update({"exp": expire.timestamp()})
    access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return access_token


def create_refresh_token(data: Mapping[str, str | float], expires_delta: timedelta | None = None) -> Any:
    to_encode = dict(data)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode.update({"exp": expire.timestamp()})
    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return refresh_token


async def service_login(
    request_data: UserLoginResponse,
) -> dict[str, str]:
    try:
        user = await User.verify_user(request_data.email, request_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="UNAUTHORIZED - Invalid User")
    except HTTPException:
        raise HTTPException(status_code=400, detail="Bad Request - Invalid User")

    user_data = await User.get(email=request_data.email)

    try:
        token = await redis.get(f"user:{user_data.id}")
        if token is not None:
            await redis.delete(f"user:{user_data.id}")

    except DoesNotExist:
        pass

    access_token_data = {"sub": str(user_data.id), "email": user_data.email}
    refresh_token_data = {"sub": "re-" + str(user_data.id) + "-er", "type": "refresh"}

    access_token = create_access_token(data=access_token_data, expires_delta=timedelta(minutes=5))
    refresh_token = create_refresh_token(data=refresh_token_data, expires_delta=timedelta(days=1))

    await redis.set(f"user:{user_data.id}", refresh_token)
    await redis.expire(f"user:{user_data.id}", timedelta(days=1))

    return {"user": str(user_data.id), "access_token": access_token, "refresh_token": refresh_token}


async def service_token_refresh(current_refresh: str) -> dict[str, str]:
    user_token = jwt.decode(current_refresh, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    user_id = user_token["sub"].split("-")[1]
    server_token = jwt.decode(await redis.get(f"user:{user_id}"), settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    server_id = server_token["sub"].split("-")[1]

    if user_id == server_id:
        user_data = await User.get(id=server_token["sub"].split("-")[1])
        access_token_data = {"sub": str(user_data.id), "email": user_data.email}
        access_token = create_access_token(data=access_token_data, expires_delta=timedelta(minutes=5))

        return {"user": str(user_data.id), "access_token": access_token}

    raise HTTPException(status_code=401, detail="UNAUTHORIZED - Invalid Token")


async def service_create_coin(request_data: UserCoinCreateResponse, current_user: int) -> None:
    await User.update_by_user_coin(request_data, current_user)


# JWT 토큰을 검증하고 user_id를 반환하는 함수
async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception


async def get_current_refresh(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        payload.get("type")
        return token
    except JWTError:
        raise credentials_exception


async def service_get_user_detail(current_user: int) -> UserGetProfileResponse:
    user = await User.get_by_user_id(current_user)
    if not user:
        raise HTTPException(status_code=404, detail="Not Found - User not found")
    main_address = await Address.get_main_address_by_user_id(current_user)
    images = await service_get_images("user", user.id)
    if len(images) == 0:
        return UserGetProfileResponse(
            email=user.email,
            name=user.name,
            nickname=user.nickname,
            contact=user.contact,
            coin=user.coin,
            created_at=user.created_at,
            updated_at=user.updated_at,
            gender=user.gender,
            age=user.age,
            content=user.content,
            address=f"{main_address.address} {main_address.detail_address}" if main_address else "",
            image=None,
        )
    else:
        image_urls = [img.url for img in images]
    return UserGetProfileResponse(
        email=user.email,
        name=user.name,
        nickname=user.nickname,
        contact=user.contact,
        coin=user.coin,
        created_at=user.created_at,
        updated_at=user.updated_at,
        gender=user.gender,
        age=user.age,
        content=user.content,
        address=f"{main_address.address} {main_address.detail_address}" if main_address else "",
        image=image_urls[0],
    )


async def service_update_user_detail(
    request_data: UserUpdateProfileResponse,
    current_user: int,
) -> UserUpdateProfileResponse:

    try:
        # 사용자 업데이트
        user = await User.update_by_user(request_data, current_user)

        return UserUpdateProfileResponse(
            nickname=user.nickname,
            contact=user.contact,
            content=user.content,
        )

    except DoesNotExist:
        # 사용자가 존재하지 않는 경우
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    except IntegrityError as e:
        # 데이터베이스 제약 조건 위반 등
        raise HTTPException(status_code=400, detail=f"데이터베이스 오류: {str(e)}")

    except ValidationError as e:
        # 유효성 검사 오류
        raise HTTPException(status_code=400, detail=f"유효하지 않은 데이터: {str(e)}")


async def service_update_user_image(file: UploadFile, current_user: int) -> dict[str, str]:
    if file is not None:
        image_url = await service_upload_image(file, "user")
        try:
            image = await Image.get(component="user", target_id=current_user)

            setattr(image, "url", image_url)

            await image.save()

            return {"message": f"{image.component} image is save to s3"}

        except DoesNotExist:
            item_data = ImageResponse(
                component="user", target_id=current_user, description=file.filename, url=image_url
            )
            await Image.create_image(request_data=item_data)
            return {"message": "'user' image is save to s3"}
