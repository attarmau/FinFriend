import requests
import os

REDDIT_HEADERS = {"User-Agent": "finfriend-bot"}
NEWSAPI_KEY = os.getenv("NEWS_API_KEY")

def fetch_reddit_posts(subreddit="investing", limit=5):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    res = requests.get(url, headers=REDDIT_HEADERS)
    posts = res.json()["data"]["children"]
    return [p["data"]["title"] + "\n" + p["data"]["selftext"] for p in posts]

def fetch_news_articles(query="stocks", page_size=5):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={NEWSAPI_KEY}"
    res = requests.get(url)
    articles = res.json()["articles"]
    return [a["title"] + "\n" + a["description"] for a in articles if a["description"]]
