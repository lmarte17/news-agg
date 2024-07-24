from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_
from ...domain.article.entities import Article
from ...domain.article.repositories import ArticleRepository
from ..models.article import ArticleModel

class SQLAlchemyArticleRepository(ArticleRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, article: Article) -> None:
        db_article = ArticleModel(**article.__dict__)
        self.session.add(db_article)
        self.session.commit()

    def get_by_id(self, id: int) -> Optional[Article]:
        db_article = self.session.query(ArticleModel).filter(ArticleModel.id == id).first()
        if db_article:
            article_data = {key: value for key, value in db_article.__dict__.items() if key != '_sa_instance_state'}
            return Article(**article_data)
        return None
    
    def get_by_url(self, url: str) -> Optional[Article]:
        db_article = self.session.query(ArticleModel).filter(ArticleModel.url == url).first()
        if db_article:
            article_data = {key: value for key, value in db_article.__dict__.items() if key != '_sa_instance_state'}
            return Article(**article_data)
        return None

    def get_latest(self, limit: int = 20) -> List[Article]:
        db_articles = self.session.query(ArticleModel).order_by(ArticleModel.published_date.desc()).limit(limit).all()
        articles = []
        for db_article in db_articles:
            article_data = {key: value for key, value in db_article.__dict__.items() if key != '_sa_instance_state'}
            articles.append(Article(**article_data))
        return articles
    
    def search(self, search_term: str) -> List[Article]:
        db_articles = self.session.query(ArticleModel).filter(
            or_(
                ArticleModel.title.ilike(f"%{search_term}%"),
                ArticleModel.summary.ilike(f"%{search_term}%")
            )
        ).all()
        articles = []
        for db_article in db_articles:
            article_data = {key: value for key, value in db_article.__dict__.items() if key != '_sa_instance_state'}
            articles.append(Article(**article_data))
        return articles