from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ....infrastructure.scraping.web_scraper import WebScraper
from ....infrastructure.repositories.sqlalchemy_article_repository import SQLAlchemyArticleRepository
from ....infrastructure.database import get_db
from .....schemas.article import ArticleSchema as Article
from .....schemas.article import ArticlesResponse
from ....infrastructure.logging import logger

router = APIRouter()

@router.get("/", response_model=ArticlesResponse)
def read_articles(db: Session = Depends(get_db), limit: int = 20):
    repository = SQLAlchemyArticleRepository(db)
    articles = repository.get_latest(limit)
    return {"articles": articles}

@router.get("/api/articles", response_model=ArticlesResponse)
async def get_articles(
    search: Optional[str] = Query(None, description="Search term for filtering articles"),
    db: Session = Depends(get_db), 
    limit: int = 20
):
    repository = SQLAlchemyArticleRepository(db)
    if search:
        articles = repository.search(search_term=search)
    else:
        articles = repository.get_latest(limit)
    return  {'articles':  articles}
    

@router.post("/scrape")
async def trigger_scrape(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    print("scraping files")
    def scrape():
        repository = SQLAlchemyArticleRepository(db)
        print("Scraping articles...")
        scraper = WebScraper(repository)
        print("Scraped articles")
        new_articles_count = scraper.scrape_articles()
        logger.info(f"Scraped {new_articles_count} new articles")

    background_tasks.add_task(scrape)
    return {"message": "Scraping task has been queued"}