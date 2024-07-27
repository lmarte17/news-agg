from ..infrastructure.db_init import init_db
from ..infrastructure.database import engine, Base
from ..infrastructure.logging import logger

def reset_database():
    logger.info("Resetting database...")
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    logger.info("All tables dropped.")

    # Re-create tables and perform initial scrape
    init_db()
    logger.info("Database reset complete.")

if __name__ == "__main__":
    reset_database()