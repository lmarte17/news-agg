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

    def __post_init__(self):
        if not self.url or not self.source:
            raise ValueError("Article must have a Source and URL")