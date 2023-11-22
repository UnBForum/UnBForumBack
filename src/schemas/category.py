import re
from datetime import datetime

from pydantic import BaseModel, field_validator


class CategoryCreateSchema(BaseModel):
    name: str
    color: str = "#10B981"

    @field_validator('color')
    @classmethod
    def validate_color(cls, color: str):
        if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
            raise ValueError('Cor inválida')
        return color


class CategoryRetrieveSchema(BaseModel):
    id: int
    name: str
    color: str
    created_at: datetime
    updated_at: datetime
