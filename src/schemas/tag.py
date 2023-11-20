
from pydantic import BaseModel


class TagCreateSchema(BaseModel):
    name: str


class TagRetrieveSchema(BaseModel):
    id: int
    name: str
