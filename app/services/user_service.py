import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.dtos.user_response import SendVerificationCodeResponse

GMAIL_USERNAME: str = "its.verified.test@gmail.com"
GMAIL_PASSWORD: str = "goxvdsfjrovuyqzv"


def generate_verification_code() -> int:
    uuid_str = uuid.uuid4().hex  # UUID 생성
    # 16진수 문자열을 10진수로 변환하여 6자리의 숫자로 제한
    numeric_token = int(uuid_str, 16) % 900000 + 100000
    return numeric_token


def send_verification_email(request_data: SendVerificationCodeResponse) -> dict[str, str]:
    try:
        verification_code = generate_verification_code()
        email_content = f"""
        안녕하세요 {request_data.name}님! 우리동네 경매장 입니다!
        
        본 이메일은 저희 서비스를 사용하기 위한 필수 사항입니다.
        
        아래의 코드는 절대 타인에게 노출되지 않도록 주의 바랍니다.
        
        코드입력과 함께 회원가입 절차를 완료하여 주시기 바랍니다.
        
        인증코드 : {verification_code}
        
        감사합니다.
        
        우리동데 경매장
        """
        msg = MIMEMultipart()
        msg["From"] = GMAIL_USERNAME
        msg["To"] = request_data.email
        msg["Subject"] = "우리동네 경매장 이메일 인증코드"

        msg.attach(MIMEText(email_content, "plain"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        server.sendmail(GMAIL_USERNAME, request_data.email, msg.as_string())
        server.close()

        return {"message": "Successfully sent the verification code to user email"}

    except Exception as e:
        raise e
