# FinFriend: Your Financial Chatbot
A chatbot that serves up daily bites of financial gossip and trending market talk. It pulls the juiciest stuff from Reddit, Twitter, and news sites, then breaks it all down using LangChain with a RAG setup

## Scenario
### Daily Market Briefings:
"Here’s what Reddit and Bloomberg are buzzing about today: TSLA earnings beat, Fed still hawkish, crypto dip alert ⚠️"

### Explain Like I’m 25 (ELI25):
"What’s going on with inflation?"
The bot searches recent posts, summarizes them in a Gen Z-friendly tone, and optionally adds sources

### "What’s Hot Today" Tracker:
Finds what people are talking about most (tickers, ETFs, sectors) based on keyword spike detection

### Ask Me Anything (with receipts):
"What’s the sentiment on NVDA this week?"
RAG pulls Reddit threads + news snippets and lets the LLM answer with a reference trail

## Folder Structure
finfriend-rag-bot/
├── app/
│   ├── main.py             
│   ├── chat_engine.py         # Core LangChain RAG logic
│   ├── retriever.py         
│   ├── summarizer.py          
│   ├── vectorstore.py         
│   └── prompts.py             
│
├── data/
│   └── sources/               
│
├── scripts/
│   └── fetch_data.py          # Scraper: Reddit, NewsAPI, Twitter
│
├── requirements.txt
├── README.md
└── .env                       
