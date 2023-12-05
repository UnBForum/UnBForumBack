from typing import List
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schemas.user import UserRetrieveSchema


class CommentCreateSchema(BaseModel):
    content: str
    files: List[str] = []


class CommentRetrieveSchema(BaseModel):
    id: int
    content: str
    is_fixed: bool
    author: UserRetrieveSchema
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentRatingSchema(BaseModel):
    rating: int
