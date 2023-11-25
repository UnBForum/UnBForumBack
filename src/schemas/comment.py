from typing import List
from datetime import datetime

from pydantic import BaseModel, field_validator

# from src.schemas.user import UserRetrieveSchema


class CommentCreateSchema(BaseModel):
    content: str
    files: List[str] = []


class CommentRetrieveSchema(BaseModel):
    id: int
    content: str
    is_fixed: bool
    # user: UserRetrieveSchema
    created_at: datetime
    updated_at: datetime
