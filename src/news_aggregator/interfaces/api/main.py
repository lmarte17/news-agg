from typing import Optional
from fastapi import FastAPI, Depends, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from prometheus_client import start_http_server, Summary, Counter, Gauge
from .routers import articles
from ...infrastructure.db_init import init_db
from ...infrastructure.logging import logger
from ....schemas.article import ArticlesResponse
from ...infrastructure.utilities.scheduler import setup_scheduler
from ...infrastructure.repositories.sqlalchemy_article_repository import SQLAlchemyArticleRepository
from ...infrastructure.database import get_db


app = FastAPI()
templates = Jinja2Templates(directory="templates")

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
IN_PROGRESS = Gauge('in_progress_requests', 'Number of requests in progress')

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database on startup...")
    init_db()
    setup_scheduler()

# Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")
logger.info("mounting Static files")

# Include routers
app.include_router(articles.router, prefix="/articles", tags=["articles"])

@app.get("/", response_class=HTMLResponse)
@REQUEST_TIME.time()
@IN_PROGRESS.track_inprogress()
async def read_root(
    request: Request, 
    search: Optional[str] = Query(None, description="Search term for filtering articles"),
    db: Session = Depends(get_db)
):
    repository = SQLAlchemyArticleRepository(db)
    articles = repository.search(search_term=search) if search else repository.get_latest(20)
    # articles = repository.get_latest(20)
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles}) 
