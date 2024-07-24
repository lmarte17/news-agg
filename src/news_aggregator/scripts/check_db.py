from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from ...config import settings
from ..infrastructure.models.article import ArticleModel

def check_db():
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    inspector = inspect(engine)
    
    print("Tables in the database:")
    print(inspector.get_table_names())
    
    print("\nColumns in the articles table:")
    for column in inspector.get_columns('articles'):
        print(f"- {column['name']} ({column['type']})")
    
    with SessionLocal() as session:
        article_count = session.query(ArticleModel).count()
        print(f"\nTotal number of articles: {article_count}")
        
        if article_count > 0:
            print("\nFirst 5 articles:")
            articles = session.query(ArticleModel).limit(5).all()
            for article in articles:
                print(f"- {article.title} ({article.url})")

if __name__ == "__main__":
    check_db()