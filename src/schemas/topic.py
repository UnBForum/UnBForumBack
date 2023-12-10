from typing import List, Optional
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter

from src.db.models import Topic
from src.schemas.category import CategoryRetrieveSchema, CategoryFilterSchema
from src.schemas.comment import CommentRetrieveSchema
from src.schemas.user import UserRetrieveSchema
from src.schemas.file import FileRetrieveSchema


class TopicCreateSchema(BaseModel):
    title: str
    content: str
    is_fixed: bool = False
    files: List[int] = []
    categories: List[int] = []


class TopicRetrieveSchema(BaseModel):
    id: int
    title: str
    content: str
    is_fixed: bool
    rating: int
    current_user_rating: Optional[int] = None
    current_user_has_saved: Optional[bool] = None
    comments_count: int
    author: UserRetrieveSchema
    files: List[FileRetrieveSchema]
    categories: List[CategoryRetrieveSchema]
    created_at: datetime
    updated_at: datetime


class TopicWithCommentsSchema(TopicRetrieveSchema):
    comments: List[CommentRetrieveSchema]


class TopicRatingSchema(BaseModel):
    rating: int
    current_user_rating: int


class TopicUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class TopicFilterSchema(Filter):
    search: Optional[str] = Field(Query(None, description='Pesquisa por título ou conteúdo'))
    order_by: Optional[List[str]] = ['-created_at']
    is_fixed: Optional[bool] = None
    category: Optional[CategoryFilterSchema] = FilterDepends(with_prefix('category', CategoryFilterSchema))

    class Constants(Filter.Constants):
        model = Topic
        search_model_fields = ['title', 'content']
