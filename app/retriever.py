import os
import requests
import yfinance as yf
from datetime import datetime, timedelta
import streamlit as st
import tweepy

REDDIT_HEADERS = {"User-Agent": "finfriend-bot"}
NEWSAPI_KEY = st.secrets.get("NEWS_API_KEY")
TWITTER_BEARER_TOKEN = st.secrets.get("TWITTER_BEARER_TOKEN")

def fetch_reddit_posts(subreddit="investing", limit=5):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    res = requests.get(url, headers=REDDIT_HEADERS)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch Reddit posts: {res.status_code}")
    posts = res.json()["data"]["children"]
    return [f"[Reddit] {p['data']['title']}\n{p['data']['selftext']}" for p in posts]

def fetch_news_articles(query="stocks", page_size=5):
    if not NEWSAPI_KEY:
        raise ValueError("Missing NEWS_API_KEY in secrets.toml or environment variables.")
    
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={NEWSAPI_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch News articles: {res.status_code}")
    articles = res.json()["articles"]
    return [f"[News] {a['title']}\n{a['description']}" for a in articles if a.get("description")]

def fetch_yahoo_finance_data(ticker="AAPL", days=3):
    end = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        raise Exception(f"No Yahoo Finance data found for {ticker}.")
    return [
        f"[Yahoo Finance] {ticker} | {row.name.date()} | Open: {row.Open:.2f}, Close: {row.Close:.2f}"
        for _, row in df.iterrows()
    ]

def fetch_twitter_finance_posts(query="finance OR stock market OR bitcoin OR investment", max_results=10):
    if not TWITTER_BEARER_TOKEN:
        raise ValueError("Missing TWITTER_BEARER_TOKEN in secrets.toml or environment variables.")
    
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
    
    tweets = client.search_recent_tweets(query=query + " -is:retweet lang:en", max_results=max_results)
    
    if not tweets.data:
        return []

    return [f"[Twitter] {tweet.text}" for tweet in tweets.data]
