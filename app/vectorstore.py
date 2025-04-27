import os
import faiss
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from app.retriever import fetch_reddit_posts, fetch_news_articles, fetch_yahoo_finance_data, fetch_twitter_finance_mock

VECTORSTORE_PATH = "data/chroma_db"

def load_data():
    reddit_docs = fetch_reddit_posts()
    news_docs = fetch_news_articles()
    yahoo_docs = fetch_yahoo_finance_data()
    twitter_docs = fetch_twitter_finance_mock()

    combined = reddit_docs + news_docs + yahoo_docs + twitter_docs
    return [Document(page_content=doc) for doc in combined]

def get_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        print("Loading Chroma DB from disk...")
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(persist_directory=VECTORSTORE_PATH, embedding_function=embeddings)
    else:
        print("Rebuilding Chroma DB...")
        docs = load_data()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=VECTORSTORE_PATH)
        vectorstore.persist()

    return vectorstore
