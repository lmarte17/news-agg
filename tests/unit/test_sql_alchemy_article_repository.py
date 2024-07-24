import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.news_aggregator.infrastructure.database import Base
from src.news_aggregator.infrastructure.repositories.sqlalchemy_article_repository import SQLAlchemyArticleRepository
from src.news_aggregator.domain.article.entities import Article

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_add_article(db_session):
    repository = SQLAlchemyArticleRepository(db_session)
    article = Article(
        id=None,
        title="Test Article",
        url="https://example.com/test",
        summary="This is a test article",
        source="Test Source",
        published_date=datetime.now(),
        created_at=datetime.now()
    )
    repository.add(article)
    
    added_article = repository.get_by_url("https://example.com/test")
    assert added_article is not None
    assert added_article.title == "Test Article"

def test_search_articles(db_session):
    repository = SQLAlchemyArticleRepository(db_session)
    # Add some test articles
    for i in range(5):
        article = Article(
            id=None,
            title=f"Test Article {i}",
            url=f"https://example.com/test{i}",
            summary=f"This is test article {i}",
            source="Test Source",
            published_date=datetime.now(),
            created_at=datetime.now()
        )
        repository.add(article)
    
    # Search for articles
    results = repository.search("Test Article")
    assert len(results) == 5

    results = repository.search("Article 3",)
    assert len(results) == 1
    assert results[0].title == "Test Article 3"