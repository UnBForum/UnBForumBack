from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from src.utils.enumerations import Role


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    role: Role = Field(default='member')
    password: str


class UserRetrieveSchema(BaseModel):
    id: int
    name: str
    email: str
    role: Role
    created_at: datetime
    updated_at: datetime


class TokenData(BaseModel):
    access_token: str
    token_type: str


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
