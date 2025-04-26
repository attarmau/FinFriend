import os
import requests
import yfinance as yf
from datetime import datetime, timedelta
import streamlit as st

REDDIT_HEADERS = {"User-Agent": "finfriend-bot"}
NEWSAPI_KEY = st.secrets["NEWS_API_KEY"]

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

def fetch_yahoo_finance_data(ticker="AAPL", days=3):
    end = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(ticker, start=start, end=end)
    return [f"{ticker} | {row.name.date()} | Open: {row.Open}, Close: {row.Close}" for _, row in df.iterrows()]
