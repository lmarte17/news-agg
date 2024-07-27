from sqlalchemy import inspect
from .database import Base, engine, SessionLocal
from .logging import logger
from .scraping.web_scraper import WebScraper
from ..infrastructure.repositories.sqlalchemy_article_repository import SQLAlchemyArticleRepository

def init_db():
    logger.info("Initializing database...")
    try:
        inspector = inspect(engine)
        db = SessionLocal()
        if not inspector.has_table('articles'):
            Base.metadata.create_all(bind=engine)
        else:
            logger.info("Table 'articles' already exists. Skipping creation.")
            logger.info("Articles table is empty. Running initial scrape...")
            repository = SQLAlchemyArticleRepository(db)
            scraper = WebScraper(repository)
            new_articles_count = scraper.scrape_articles()
            logger.info(f"Initial scrape completed. {new_articles_count} articles added.")    
    except Exception as e:
        logger.error(f"An error occurred while initializing the database: {str(e)}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_db()