from datetime import datetime

from pydantic import BaseModel


class FileRetrieveSchema(BaseModel):
    id: int
    name: str
    content_type: str
    upload_path: str
    created_at: datetime
    updated_at: datetime
