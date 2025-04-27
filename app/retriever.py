import os
import requests
import yfinance as yf
from datetime import datetime, timedelta
import time
import streamlit as st
import tweepy

REDDIT_CLIENT_ID = st.secrets.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = st.secrets.get("REDDIT_CLIENT_SECRET")
NEWSAPI_KEY = st.secrets.get("NEWS_API_KEY")
TWITTER_BEARER_TOKEN = st.secrets.get("TWITTER_BEARER_TOKEN")

REDDIT_USER_AGENT = "finfriend-bot/1.0 (by u/Imaginary-Weird-7959)"

def fetch_with_retry(url, retries=5, backoff_factor=2, headers=None, data=None, auth=None):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, headers=headers, data=data, auth=auth)
            if response.status_code == 429:  
                raise Exception("Rate limit exceeded. Retrying...")
            response.raise_for_status() 
            return response
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                backoff_time = backoff_factor ** attempt  
                print(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
            else:
                raise Exception(f"All {retries} retry attempts failed.")

def choose_ticker(user_question):
    question = user_question.lower()
    if "apple" in question or "aapl" in question:
        return "AAPL"
    elif "tesla" in question or "tsla" in question:
        return "TSLA"
    elif "microsoft" in question or "msft" in question:
        return "MSFT"
    elif "amazon" in question or "amzn" in question:
        return "AMZN"
    elif "inflation" in question or "economy" in question:
        return "^GSPC"  
    else:
        return None

def fetch_reddit_posts(subreddit="investing", limit=5):
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        raise ValueError("Missing REDDIT_CLIENT_ID or REDDIT_SECRET in secrets.toml.")
    
    auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": REDDIT_USER_AGENT}
    
    token_res = fetch_with_retry("https://www.reddit.com/api/v1/access_token", retries=3, headers=headers, data=data, auth=auth)
    token = token_res.json().get("access_token")
    headers["Authorization"] = f"bearer {token}"  
    url = f"https://oauth.reddit.com/r/{subreddit}/hot?limit={limit}"
    
    res = fetch_with_retry(url, retries=3, headers=headers)
    posts = res.json().get("data", {}).get("children", [])
    
    return [f"[Reddit] {p['data']['title']}\n{p['data']['selftext']}" for p in posts]

def fetch_news_articles(query="stocks", page_size=5):
    if not NEWSAPI_KEY:
        raise ValueError("Missing NEWS_API_KEY in secrets.toml or environment variables.")
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={NEWSAPI_KEY}"
    
    res = fetch_with_retry(url, retries=3)
    articles = res.json().get("articles", [])
    
    return [f"[News] {a['title']}\n{a['description']}" for a in articles if a.get("description")]

def fetch_yahoo_finance_data(ticker, days=5):
    end = datetime.today()
    start = end - timedelta(days=days + 2)
    yf_ticker = ticker.replace("^", "%5E") if ticker.startswith("^") else ticker
    
    try:
        df = yf.download(yf_ticker, start=start, end=end, progress=False, auto_adjust=True)
    except Exception as e:
        print(f"Error fetching Yahoo Finance data: {e}")
        return []
    
    if df.empty:
        return [] 

    return [
        f"[Yahoo Finance] {ticker} | {row.name.date()} | Open: {row.Open:.2f}, Close: {row.Close:.2f}"
        for _, row in df.iterrows()
    ]

def fetch_twitter_finance_posts(query="finance OR stock market OR bitcoin OR investment", max_results=10):
    if not TWITTER_BEARER_TOKEN:
        raise ValueError("Missing TWITTER_BEARER_TOKEN in secrets.toml or environment variables.")
    
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
    
    try:
        tweets = client.search_recent_tweets(query=query + " -is:retweet lang:en", max_results=max_results)
    except Exception as e:
        print(f"Error fetching Twitter posts: {e}")
        return []
    
    if not tweets.data:
        return []
    
    return [f"[Twitter] {tweet.text}" for tweet in tweets.data]

st.title("📈 FinFriend - Your Finance Buddy")
user_question = st.text_input("Ask me anything about stocks, finance, or economy:")

if user_question:
    try:
        ticker = choose_ticker(user_question)
        if ticker:
            yahoo_info = fetch_yahoo_finance_data(ticker)
        else:
            yahoo_info = [] 
        
        reddit_posts = fetch_reddit_posts()
        news_articles = fetch_news_articles(query=user_question)
        twitter_posts = fetch_twitter_finance_posts(query=user_question)

        if reddit_posts:
            st.subheader("🔥 Reddit Highlights")
            for post in reddit_posts:
                st.write(post)
        
        if news_articles:
            st.subheader("📰 Latest News")
            for article in news_articles:
                st.write(article)

        if twitter_posts:
            st.subheader("🐦 Twitter Buzz")
            for tweet in twitter_posts:
                st.write(tweet)

        if yahoo_info:
            st.subheader("💹 Stock Prices")
            for stock in yahoo_info:
                st.write(stock)

    except Exception as e:
        st.error(f"Sorry, something went wrong: {e}")
