import logging
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.configs import settings
from app.dtos.user_response import SendVerificationCodeResponse
from app.utils.redis_ import redis
import orjson


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

        code = redis.get(request_data.email)['code']

        if code is None:
            await redis.set(request_data.email, orjson.dumps({"email": request_data.email, "code": verification_code}))
            await redis.expire(request_data.email, 60)

        elif len(code) == 6:
            await redis.delete(request_data.email)
            await redis.set(request_data.email, orjson.dumps({"email": request_data.email, "code": verification_code}))
            await redis.expire(request_data.email, 60)

        server.sendmail(settings.GMAIL_USERNAME, request_data.email, msg.as_string())
        server.close()

        return {"message": "Successfully sent the verification code to user email"}

    except Exception as e:
        logging.error(f"An error occurred while sending verification email: {e}")
        return {"error": str(e)}
