import pytest
from datetime import datetime
from src.news_aggregator.domain.article.entities import Article

def test_article_creation():
    article = Article(
        id=1,
        title="Test Article",
        url="https://example.com/test",
        summary="This is a test article",
        source="Test Source",
        published_date=datetime.now(),
        created_at=datetime.now()
    )
    assert article.id == 1
    assert article.title == "Test Article"
    assert article.url == "https://example.com/test"
    assert article.summary == "This is a test article"
    assert article.source == "Test Source"

def test_article_invalid_creation():
    with pytest.raises(ValueError):
        Article(
            id=1,
            title="Test Article",  
            url="https://example.com/test",
            summary="This is a test article",
            source="", # Empty source should raise ValueError
            published_date=datetime.now(),
            created_at=datetime.now()
        )