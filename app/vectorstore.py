import os
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from app.retriever import fetch_reddit_posts, fetch_news_articles

# Optional: load from a folder or use a loader
from app.retriever import fetch_reddit_posts, fetch_news_articles

VECTORSTORE_PATH = "data/faiss_index"

def load_data():
    reddit_docs = fetch_reddit_posts()
    news_docs = fetch_news_articles()
    combined = reddit_docs + news_docs

    return [Document(page_content=doc) for doc in combined]

def get_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        print("Loading FAISS index from disk...")
        vectorstore = FAISS.load_local(VECTORSTORE_PATH, OpenAIEmbeddings())
    else:
        print("Rebuilding FAISS index...")
        docs = load_data()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(VECTORSTORE_PATH)

    return vectorstore
