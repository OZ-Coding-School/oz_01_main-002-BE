from typing import Optional

from pydantic import BaseModel


class UserSignUpResponse(BaseModel):
    name: str
    email: str
    password: str
    gender: str
    age: int
    contact: str
    nickname: str


class SendVerificationCodeResponse(BaseModel):
    name: str
    email: str


class VerifyEmailResponse(BaseModel):
    email: str
    code: int


class VerifyNicknameResponse(BaseModel):
    nickname: str


class VerifyContactResponse(BaseModel):
    contact: str


class UserLoginResponse(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    token_type: str
    token: str
