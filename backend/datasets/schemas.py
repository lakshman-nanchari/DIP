from pydantic import BaseModel
from datetime import datetime


class DatasetResponse(BaseModel):
    id: int
    name: str
    file_type: str
    rows: int | None
    columns: int | None
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True