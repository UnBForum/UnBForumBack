from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from src.schemas.user import UserRetrieveSchema


class CommentCreateSchema(BaseModel):
    content: str
    files: List[str] = []


class CommentRetrieveSchema(BaseModel):
    id: int
    content: str
    is_fixed: bool
    rating: int
    current_user_rating: Optional[int] = None
    author: UserRetrieveSchema
    created_at: datetime
    updated_at: datetime


class CommentRatingSchema(BaseModel):
    rating: int
    current_user_rating: int
