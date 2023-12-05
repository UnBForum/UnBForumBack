from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

from src.utils.enumerations import Role
from src.schemas.tag import TagRetrieveSchema


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    role: Role = Field(default='member')
    password: str
    tags: List[str] = []

    @field_validator('email')
    @classmethod
    def validate_institutional_email(cls, email: str):
        if not email.endswith('unb.br'):
            raise ValueError('Email institucional inválido')
        return email


class UserChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str


class UserRetrieveSchema(BaseModel):
    id: int
    name: str
    email: str
    role: Role
    tags: List[TagRetrieveSchema]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
