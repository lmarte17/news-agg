import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fuzzywuzzy import fuzz
from ...domain.article.entities import Article
# from ...domain.article.repositories import ArticleRepository
from ...infrastructure.repositories.sqlalchemy_article_repository import SQLAlchemyArticleRepository
from ...infrastructure.database import SessionLocal
from ....config import settings
from ...application.nlp.sentiment_analysis import analyze_sentiment
from ...rabbitmq.publisher import publish_message

class WebScraper:
    def __init__(self, article_repository: SQLAlchemyArticleRepository):
        self.article_repository = article_repository

    def scrape_articles(self) -> int:
        response = requests.get(settings.NEWS_SOURCE_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        new_articles_count = 0
        news_tables = soup.find_all('table', class_='news')
        
        
        # Function to check for duplicates using fuzzy comparison
        def is_duplicate(new_article, articles, threshold=90):
            for article in articles:
                title_similarity = fuzz.ratio(new_article['title'], article['title'])
                url_similarity = fuzz.ratio(new_article['url'], article['url'])
                if title_similarity > threshold or url_similarity > threshold:
                    return True
            return False
        
        articles = []
        for table in news_tables:
            td_news = table.find_all('td', class_='news')
            for td in td_news:
                divs = td.find_all('div', class_=lambda x: x not in ['clear', 'content']) 
                for div in divs:
                    links = div.find_all('a', href=True)
                    for link in links:
                        title = link.get_text(strip=True)
                        url = link['href']
                        summary = "Summary placeholder"  # Placeholder for the summary
                        sentiment = analyze_sentiment(title)
                        new_article = {"title": title, "url": url, "summary": summary}
                        if not is_duplicate(new_article, articles):
                            articles.append(new_article)
                            # Check if article already exists
                            existing_article = self.article_repository.get_by_url(url)
                            if not existing_article:
                                article = Article(
                                    id=None,
                                    title=title,
                                    url=url,
                                    summary=summary, # You might want to fetch and parse the summary
                                    source=url,
                                    published_date=datetime.now(),  # You might want to parse the actual publication date
                                    created_at=datetime.now(),
                                    sentiment=sentiment
                                    )
                                self.article_repository.add(article)
                                article_dict = article.to_dict()
                                publish_message('article_queue', article_dict)
                                new_articles_count += 1

        return new_articles_count