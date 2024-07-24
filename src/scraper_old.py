from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz

def scrape_articles():
    url = 'https://lithosgraphein.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    news_tables = soup.find_all('table', class_='news')

    articles = []
    # Function to check for duplicates using fuzzy comparison
    def is_duplicate(new_article, articles, threshold=90):
        for article in articles:
            title_similarity = fuzz.ratio(new_article['title'], article['title'])
            url_similarity = fuzz.ratio(new_article['url'], article['url'])
            if title_similarity > threshold or url_similarity > threshold:
                return True
        return False

    # Loop through each news table and find the relevant article links and titles
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
                    new_article = {"title": title, "url": url, "summary": summary}
                    if not is_duplicate(new_article, articles):
                        articles.append(new_article)

    return articles