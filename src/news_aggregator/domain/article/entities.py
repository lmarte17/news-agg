from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    id: int
    title: str
    url: str
    summary: str
    source: str
    published_date: datetime
    created_at: datetime
    sentiment: Optional[str] = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "summary": self.summary,
            "source": self.source,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "sentiment": self.sentiment,
        }

    def __post_init__(self):
        if not self.url or not self.source:
            raise ValueError("Article must have a Source and URL")