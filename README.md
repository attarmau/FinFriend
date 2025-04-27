# FinFriend: Your Financial Chatbot
FinFriend is a chatbot designed to deliver real-time financial insights by leveraging data from Reddit, Twitter, news sites, and Yahoo Finance. The front-end of the application is powered by Streamlit, chosen for its ability to quickly prototype interactive web applications. This allows users to easily query financial data, with an intuitive and engaging UI that is fully functional while the backend is being optimised.

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

## LangChain for Smart RAG Integration
The core of the chatbot’s intelligence comes from integrating a Retrieval-Augmented Generation (RAG) setup, where LangChain plays a crucial role. LangChain enables the chatbot to efficiently pull and process information from multiple external sources, allowing it to generate accurate and contextually relevant responses. The ability to handle diverse data inputs from various sources ensures the chatbot’s adaptability to real-time trends and updates in the financial space.

<img width="861" alt="Screenshot 2025-04-27 at 10 32 30 PM" src="https://github.com/user-attachments/assets/57e97b8c-ee0a-444a-8789-6813875a9050" />

## Pinecone for Fast Document Retrieval
For handling large datasets and ensuring high-performance document retrieval, Pinecone was incorporated to manage vector search. Pinecone's capability to perform fast similarity searches and retrieve relevant documents efficiently is essential, particularly as the amount of financial data grows over time.

Learn more about vector databases and the different options by referring to:
https://medium.com/@sakhamurijaikar/which-vector-database-is-right-for-your-generative-ai-application-pinecone-vs-chromadb-1d849dd5e9df

<img width="775" alt="Screenshot 2025-04-27 at 10 41 32 PM" src="https://github.com/user-attachments/assets/699ac148-bb70-4272-ad5e-24751072d8e3" />

Vector database intro image source: https://www.trantorinc.com/blog/pinecone-ai-guide


This project demonstrates an efficient approach to building a scalable, data-driven proof of concept (POC) for a RAG-based chatbot. By integrating advanced technologies like LangChain, Pinecone, and Streamlit, it enables the rapid development of an interactive, real-time chatbot capable of delivering accurate financial insights. This setup provides a streamlined framework for others to quickly prototype and deploy similar applications, ensuring effective handling of diverse data sources and fast document retrieval.
