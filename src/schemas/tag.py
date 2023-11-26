from datetime import datetime

from pydantic import BaseModel


class TagCreateSchema(BaseModel):
    name: str


class TagRetrieveSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
