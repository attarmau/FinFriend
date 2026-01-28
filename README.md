# FinFriend: Your Financial Chatbot

FinFriend is a chatbot designed to deliver real-time financial insights by leveraging data from Reddit, Twitter, news sites, and Yahoo Finance. The application uses a **Dynamic Agentic** approach (powered by OpenAI functions) to fetch live data on demand.

The front-end is powered by Streamlit, offering an intuitive chat interface.

## Demo
*(Insert demo link or screenshot here)*

## Features

### 📰 Daily Market Briefings
"Here’s what Reddit and Bloomberg are buzzing about today: TSLA earnings beat, Fed still hawkish, crypto dip alert ⚠️"

### 🔍 Explain Like I’m 25 (ELI25)
"What’s going on with inflation?"
The bot searches recent posts and summarizes them in a clear, friendly tone.

### 📈 "What’s Hot Today" Tracker
Finds what people are talking about most (tickers, ETFs, sectors) based on keyword spike detection.

### 🤔 Ask Me Anything (with receipts)
"What’s the sentiment on NVDA this week?"
The Agent pulls Reddit threads + news snippets and lets the LLM answer with real-time data.

## Architecture

Refactored from a static RAG to a **Dynamic Tool-Using Agent**:
- **Agent**: OpenAI GPT-4 with direct function calling.
- **Tools**:
  - `fetch_reddit_posts`: Hot threads from Subreddits.
  - `fetch_news_articles`: NewsAPI for global finance news.
  - `fetch_yahoo_finance_data`: Historical stock data.
  - `fetch_twitter_finance_posts`: Real-time tweets.
- **Frontend**: Streamlit Chat Interface.

## Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/attarmau/FinFriend.git
   cd FinFriend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**:
   > [!IMPORTANT]
   > You must create your own secrets file to run this app.
   
   Create a file `.streamlit/secrets.toml` and add your keys:
   ```toml
   OPENAI_API_KEY = "sk-..."
   REDDIT_CLIENT_ID = "..."
   REDDIT_CLIENT_SECRET = "..."
   NEWS_API_KEY = "..."
   TWITTER_BEARER_TOKEN = "..."
   ```

4. **Run the App**:
   ```bash
   streamlit run main.py
   ```
