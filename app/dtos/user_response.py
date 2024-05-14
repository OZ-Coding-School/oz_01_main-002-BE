from pydantic import BaseModel


class UserSignUpResponse(BaseModel):
    name: str
    email: str
    password: str
    gender: str
    age: int
    contact: int
    nickname: str
    content: str


class SendVerificationCodeResponse(BaseModel):
    name: str
    email: str


class VerifyEmailResponse(BaseModel):
    email: str
    code: int


class VerifyNicknameResponse(BaseModel):
    nickname: str
