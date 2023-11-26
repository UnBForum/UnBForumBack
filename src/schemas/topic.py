from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from src.schemas.category import CategoryRetrieveSchema


class TopicCreateSchema(BaseModel):
    title: str
    content: str
    is_fixed: bool = False
    files: List[str] = []
    categories: List[int] = []


class TopicRetrieveSchema(BaseModel):
    id: int
    title: str
    content: str
    is_fixed: bool
    # files: List[File]
    categories: List[CategoryRetrieveSchema]
    user_id: int
    created_at: datetime
    updated_at: datetime
    # comments: List[CommentRetrieveSchema] = []


class TopicUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
