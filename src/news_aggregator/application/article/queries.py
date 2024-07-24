from typing import List
from ...domain.article.repositories import ArticleRepository
from ...domain.article.entities import Article

class GetArticlesQuery:
    def __init__(self, article_repository: ArticleRepository):
        self.article_repository = article_repository

    def execute(self, limit: int = 20, offset: int = 0) -> List[Article]:
        return self.article_repository.list(limit, offset)