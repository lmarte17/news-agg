from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ArticleSchema(BaseModel):
    id: int
    title: str
    url: str
    summary: str
    source: str
    published_date: datetime
    created_at: datetime
    sentiment: str

    class Config:
        orm_mode = True
        
class ArticlesResponse(BaseModel):
    articles: List[ArticleSchema]