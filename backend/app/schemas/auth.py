from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

PasswordStr = Annotated[str, Field(max_length=72)]


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: PasswordStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


class Token(BaseModel):
    access_token: str
    token_type: str
