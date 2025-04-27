# FinFriend: Your Financial Chatbot
A chatbot that aggregates financial news, Reddit posts, and Twitter updates, powered by LangChain with a Retrieval-Augmented Generation (RAG) setup and Pinecone/FAISS search. The project highlights my skills in building a RAG-based chatbot with a Streamlit UI, providing an efficient proof-of-concept (POC) for fast data retrieval and interactive user experience. 

✋🏻 The functional UI is fully operational while backend refinement is underway

## Demo: https://finfriend-your-financial-chatbot.streamlit.app/
<img width="1222" alt="Screenshot 2025-04-27 at 9 37 13 PM" src="https://github.com/user-attachments/assets/91e0fa45-f71b-4561-a19b-6491c0ba9e28" />

## Scenario
### 📰 Daily Market Briefings:
"Here’s what Reddit and Bloomberg are buzzing about today: TSLA earnings beat, Fed still hawkish, crypto dip alert ⚠️"

### 🔍 Explain Like I’m 25 (ELI25):
"What’s going on with inflation?"
The bot searches recent posts, summarizes them in a Gen Z-friendly tone, and optionally adds sources

### 📈 "What’s Hot Today" Tracker:
Finds what people are talking about most (tickers, ETFs, sectors) based on keyword spike detection

### 🤔 Ask Me Anything (with receipts):
"What’s the sentiment on NVDA this week?"
RAG pulls Reddit threads + news snippets and lets the LLM answer with a reference trail
