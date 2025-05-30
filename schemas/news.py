# schemas/news.py
from pydantic import BaseModel
from datetime import datetime

class NewsOut(BaseModel):
    id: int
    title: str
    link: str
    image_url: str | None
    created_at: datetime

    class Config:
        orm_mode = True
