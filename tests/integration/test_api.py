import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.news_aggregator.infrastructure.database import Base, get_db
from src.news_aggregator.interfaces.api.main import app
from src.news_aggregator.infrastructure.repositories.sqlalchemy_article_repository import SQLAlchemyArticleRepository
from src.news_aggregator.domain.article.entities import Article
from datetime import datetime

# Use a SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Latest News" in response.text

def test_get_articles():
    # Add some test articles to the database
    db = TestingSessionLocal()
    repository = SQLAlchemyArticleRepository(db)
    for i in range(5):
        article = Article(
            id=None,
            title=f"Test Article {i}",
            url=f"https://example.com/test{i}",
            summary=f"This is test article {i}",
            source="Test Source",
            published_date=datetime.now(),
            created_at=datetime.now(),
            sentiment="Neutral"
        )
        repository.add(article)
    db.close()

    response = client.get("articles/api/articles")
    assert response.status_code == 200

def test_search_articles():
    # Add some test articles to the database
    db = TestingSessionLocal()
    repository = SQLAlchemyArticleRepository(db)
    for i in range(5):
        article = Article(
            id=None,
            title=f"Test Article {i}",
            url=f"https://example.com/test{i}",
            summary=f"This is test article {i}",
            source="Test Source",
            published_date=datetime.now(),
            created_at=datetime.now(),
            sentiment="Neutral"
        )
        repository.add(article)
    db.close()

    response = client.get("articles/api/articles?search=Article 3")
    assert response.status_code == 200