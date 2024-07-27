from typing import Optional
from fastapi import FastAPI, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .routers import articles
from ...infrastructure.db_init import init_db
from ...infrastructure.logging import logger
from ...infrastructure.utilities.scheduler import setup_scheduler
from ...infrastructure.repositories.sqlalchemy_article_repository import SQLAlchemyArticleRepository
from ...infrastructure.database import get_db


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database on startup...")
    init_db()
    setup_scheduler()

# Include routers
app.include_router(articles.router, prefix="/articles", tags=["articles"])

@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request, 
    search: Optional[str] = Query(None, description="Search term for filtering articles"),
    db: Session = Depends(get_db)
):
    repository = SQLAlchemyArticleRepository(db)
    articles = repository.search(search_term=search) if search else repository.get_latest(20)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles}) 
