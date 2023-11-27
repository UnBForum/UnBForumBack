from typing import List, Optional
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter

from src.db.models import Topic
from src.schemas.category import CategoryRetrieveSchema, CategoryFilterSchema
from src.schemas.user import UserRetrieveSchema


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
    user: UserRetrieveSchema
    # files: List[File]
    categories: List[CategoryRetrieveSchema]
    created_at: datetime
    updated_at: datetime
    # comments: List[CommentRetrieveSchema]


class TopicUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class TopicFilterSchema(Filter):
    search: Optional[str] = Field(Query(None, description='Pesquisa por título ou conteúdo'))
    order_by: Optional[List[str]] = ['-created_at']
    category: Optional[CategoryFilterSchema] = FilterDepends(with_prefix('category', CategoryFilterSchema))

    class Constants(Filter.Constants):
        model = Topic
        search_model_fields = ['title', 'content']
