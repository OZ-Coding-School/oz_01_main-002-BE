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


class UserCoinCreateResponse(BaseModel):
    coin: float


class UserGetProfileResponse(BaseModel):
    coin: float
    content: str
    address: str
    name: str
    email: str
    gender: str
    age: int
    contact: str
    nickname: str


class UserUpdateProfileResponse(BaseModel):
    nickname: Optional[str] = None
    contact: Optional[str] = None
    content: Optional[str] = None
