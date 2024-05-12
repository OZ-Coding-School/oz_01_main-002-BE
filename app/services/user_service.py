import logging
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import orjson
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.configs import settings
from app.dtos.user_response import SendVerificationCodeResponse, VerifyEmailResponse
from app.utils.redis_ import redis


def generate_verification_code() -> int:
    return int("".join(str(random.randint(0, 9)) for _ in range(6)))


async def send_verification_email(request_data: SendVerificationCodeResponse) -> dict[str, str]:
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
