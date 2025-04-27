import os
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from app.retriever import fetch_reddit_posts, fetch_news_articles, fetch_yahoo_finance_data, fetch_twitter_finance_posts
import streamlit as st

VECTORSTORE_PATH = "data/chroma_db"
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")  

def load_data():
    reddit_docs = fetch_reddit_posts(subreddit="investing", limit=5)
    news_docs = fetch_news_articles(query="stocks", page_size=5)
    yahoo_docs = fetch_yahoo_finance_data(ticker="AAPL", days=3)
    twitter_docs = fetch_twitter_finance_posts(query="finance OR stock market OR bitcoin OR investment", max_results=10)

    combined = reddit_docs + news_docs + yahoo_docs + twitter_docs
    return [Document(page_content=doc) for doc in combined]

def get_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        print("Loading Chroma DB from disk...")
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)  
        vectorstore = Chroma(persist_directory=VECTORSTORE_PATH, embedding_function=embeddings)
    else:
        print("Rebuilding Chroma DB...")
        docs = load_data()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY) 
        vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=VECTORSTORE_PATH)
        vectorstore.persist()

    return vectorstore
