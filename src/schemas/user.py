from pydantic import BaseModel, Field, EmailStr

from src.utils.enumerations import Role


class User(BaseModel):
    name: str
    email: EmailStr
    role: Role = Field(default='member')
    password: str


class TokenData(BaseModel):
    access_token: str
    token_type: str
