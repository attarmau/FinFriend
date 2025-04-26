import os
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Optional: load from a folder or use a loader
from app.retriever import fetch_reddit_posts, fetch_news_articles

VECTORSTORE_PATH = "data/faiss_index"

def load_data():
    # Combine Reddit + News into LangChain docs
    reddit_docs = fetch_reddit_posts()
    news_docs = fetch_news_articles()
    combined = reddit_docs + news_docs

    return [Document(page_content=doc) for doc in combined]

def get_vectorstore():
    # Rebuild every time for demo; cache later for prod
    docs = load_data()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore
