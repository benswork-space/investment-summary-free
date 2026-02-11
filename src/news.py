import feedparser
import requests
from urllib.parse import quote

from src.config import NEWSAPI_KEY


def fetch_google_news(query: str, max_results: int = 5) -> list:
    """Fetch news from Google News RSS for the past day."""
    url = (
        f"https://news.google.com/rss/search?"
        f"q={quote(query)}+when:1d&hl=en-US&gl=US&ceid=US:en"
    )
    try:
        feed = feedparser.parse(url)
        return [
            {
                "title": entry.get("title", ""),
                "source": entry.get("source", {}).get("title", "Unknown"),
                "published": entry.get("published", ""),
            }
            for entry in feed.entries[:max_results]
        ]
    except Exception as e:
        print(f"  Google News error for '{query}': {e}")
        return []


def fetch_newsapi(query: str, max_results: int = 5) -> list:
    """Fetch news from NewsAPI (optional, requires NEWSAPI_KEY)."""
    if not NEWSAPI_KEY:
        return []

    try:
        resp = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "sortBy": "relevance",
                "language": "en",
                "pageSize": max_results,
                "apiKey": NEWSAPI_KEY,
            },
            timeout=10,
        )
        resp.raise_for_status()
        return [
            {
                "title": a.get("title", ""),
                "source": a.get("source", {}).get("name", "Unknown"),
                "description": a.get("description", ""),
            }
            for a in resp.json().get("articles", [])[:max_results]
        ]
    except Exception as e:
        print(f"  NewsAPI error for '{query}': {e}")
        return []


def fetch_news(portfolio: dict, interest_areas: list) -> dict:
    """Fetch news for every ticker and interest area."""
    news = {"tickers": {}, "industries": {}}

    for ticker, info in portfolio.items():
        query = f"{info['name']} OR {ticker} stock"
        articles = fetch_google_news(query, 3) + fetch_newsapi(
            f"{info['name']} {ticker}", 2
        )
        if articles:
            news["tickers"][ticker] = articles

    for area in interest_areas:
        articles = fetch_google_news(f"{area} investing market", 3) + fetch_newsapi(
            f"{area} market investing", 2
        )
        if articles:
            news["industries"][area] = articles

    return news
