import logging
import random
import re
import smtplib
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Optional

import orjson
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # type: ignore
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.configs import settings
from app.dtos.terms_agreement_response import TermsAgreementCreateResponse
from app.dtos.terms_response import TermIDResponse
from app.dtos.user_response import (
    SendVerificationCodeResponse,
    TokenResponse,
    UserCoinCreateResponse,
    UserLoginResponse,
    UserSignUpResponse,
    VerifyContactResponse,
    VerifyEmailResponse,
    VerifyNicknameResponse,
)
from app.models.users import User
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
        안녕하세요 {request_data.name}님! 우리동네 경매장 입니다!
        
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


async def service_code_authentication(request_data: VerifyEmailResponse) -> None:
    try:
        email = await redis.get(request_data.email)
        if email is None:
            raise HTTPException(status_code=400, detail="Bad Request - Incorrect Email")

        elif request_data.email == orjson.loads(email)["email"]:
            if str(request_data.code) == orjson.loads(await redis.get(request_data.email))["code"]:
                await redis.delete(request_data.email)
                raise HTTPException(status_code=200, detail="OK")
        raise HTTPException(status_code=400, detail="Bad Request - Incorrect Code")

    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Bad Request - Check user email as the authentication email ")


async def service_nickname_verification(request_data: VerifyNicknameResponse) -> None:
    try:
        if request_data.nickname.isdigit():
            raise HTTPException(status_code=400, detail="Bad Request - Nickname must string")

        user = await User.get_by_user_nickname(nickname=request_data.nickname)

        if user.nickname == request_data.nickname:
            raise HTTPException(status_code=400, detail="Bad Request - Nickname already registered")

    except DoesNotExist:
        raise HTTPException(status_code=200, detail="OK - Nickname available")


async def service_contact_verification(request_data: VerifyContactResponse) -> None:
    try:
        integer_contact = ",".join(request_data.contact.split("-"))
        if not integer_contact.isdigit():
            raise HTTPException(status_code=400, detail="Bad Request - Contact must integer without '-' ")

        if not is_valid_contact(request_data.contact):
            raise HTTPException(status_code=400, detail="Bad Request - Invalid Contact")

        user = await User.get_by_user_contact(contact=request_data.contact)

        if user.contact == request_data.contact:
            raise HTTPException(status_code=400, detail="Bad Request - Contact already registered")

    except DoesNotExist:
        raise HTTPException(status_code=200, detail="OK - Contact available")


async def service_signup(request_data: UserSignUpResponse, term_data: list[TermIDResponse]) -> None:
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

        raise HTTPException(status_code=201, detail="Created - successfully signup!")

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
) -> tuple[dict[str, str], str]:
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
    refresh_token_data = {"sub": "re-" + str(user_data.id) + "-er", "email": user_data.email}

    access_token = create_access_token(data=access_token_data, expires_delta=timedelta(minutes=5))
    refresh_token = create_refresh_token(data=refresh_token_data, expires_delta=timedelta(days=1))

    await redis.set(f"user:{user_data.id}", refresh_token)
    await redis.expire(f"user:{user_data.id}", timedelta(days=1))

    return {"user": str(user_data.id), "access_token": access_token}, refresh_token


async def service_token_refresh(request_data: TokenResponse) -> dict[str, str]:
    if request_data.token_type == "refresh_token":
        user_token = jwt.decode(request_data.token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id = user_token["sub"].split("-")[1]
        server_token = jwt.decode(
            await redis.get(f"user:{user_id}"), settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        server_id = server_token["sub"].split("-")[1]

        if user_id == server_id:
            user_data = await User.get(id=server_token["sub"].split("-")[1])
            access_token_data = {"sub": str(user_data.id), "email": user_data.email}
            access_token = create_access_token(data=access_token_data, expires_delta=timedelta(minutes=5))

            return {"user": str(user_data.id), "access_token": access_token}

    raise HTTPException(status_code=401, detail="UNAUTHORIZED - Invalid Token")


async def service_create_coin(request_data: UserCoinCreateResponse, current_user: int) -> None:
    await User.update_by_user_coin(request_data, current_user)


async def service_check_token(request_data: TokenResponse) -> None:
    if request_data.token_type == "access_token":
        try:
            jwt.decode(request_data.token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            raise HTTPException(status_code=200, detail="Token is ready for use")
        except JWTError as e:
            raise HTTPException(status_code=401, detail=str(e))

    raise HTTPException(status_code=401, detail="Invalid Token")


# JWT 토큰을 검증하고 user_id를 반환하는 함수
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[int]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
