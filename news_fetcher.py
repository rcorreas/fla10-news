import feedparser
import requests
from datetime import datetime
from config import RSS_FEEDS, MAX_ARTICLES_PER_FEED

def fetch_news_from_rss():
    all_news = []
    
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:
                news_item = {
                    'title': entry.get('title', 'Sem título'),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': feed_url,
                    'fetched_at': datetime.now().isoformat()
                }
                all_news.append(news_item)
                
        except Exception as e:
            print(f"Erro ao processar feed {feed_url}: {e}")
            continue
    
    return all_news

def get_flamengo_news():
    news = fetch_news_from_rss()
    # Filtrar apenas notícias relevantes ao Flamengo
    flamengo_keywords = ['flamengo', 'fla', 'mengão', 'rubro-negro']
    
    filtered_news = []
    for item in news:
        text = f"{item['title']} {item['summary']}".lower()
        if any(keyword in text for keyword in flamengo_keywords):
            filtered_news.append(item)
    
    return filtered_news
