from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from ...infrastructure.scraping.web_scraper import WebScraper
from ...infrastructure.repositories.sqlalchemy_article_repository import SQLAlchemyArticleRepository
from ...infrastructure.database import SessionLocal
from ..logging import logger

def scheduled_scrape():
    logger.info("Starting scheduled scrape")
    db = SessionLocal()
    try:
        repository = SQLAlchemyArticleRepository(db)
        scraper = WebScraper(repository)
        new_articles_count = scraper.scrape_articles()
        logger.info(f"Scheduled scrape completed. {new_articles_count} new articles added.")
    finally:
        db.close()

def setup_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the scraper to run every hour
    scheduler.add_job(scheduled_scrape, CronTrigger(minute=0))
    scheduler.start()
    logger.info("Scheduler started")
    return scheduler