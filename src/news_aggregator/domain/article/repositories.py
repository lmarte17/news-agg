from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Article

class ArticleRepository(ABC):
    @abstractmethod
    def add(self, article: Article) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Article]:
        pass
    
    @abstractmethod
    def get_by_url(self, url: str) -> Optional[Article]:
        pass

    @abstractmethod
    def get_latest(self, limit: int) -> List[Article]:
        pass
    
    @abstractmethod
    def search(self, search_term: str) -> List[Article]:
        pass