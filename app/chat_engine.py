from openai import OpenAI
import json
import streamlit as st

from app.retriever import (
    fetch_reddit_posts,
    fetch_news_articles,
    fetch_yahoo_finance_data,
    fetch_twitter_finance_posts
)

# 1. Define Tool Functions for binding
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_reddit_posts",
            "description": "Fetches hot posts from a subreddit (e.g., investing, stocks).",
            "parameters": {
                "type": "object",
                "properties": {
                    "subreddit": {"type": "string", "description": "Subreddit name"},
                    "limit": {"type": "integer"}
                },
                "required": ["subreddit"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_news_articles",
            "description": "Fetches latest news articles matching a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "page_size": {"type": "integer"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_yahoo_finance_data",
            "description": "Fetches stock prices for a ticker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker (e.g. AAPL)"},
                    "days": {"type": "integer"}
                },
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_twitter_finance_posts",
            "description": "Fetches recent tweets for a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer"}
                },
                "required": ["query"]
            }
        }
    }
]

TOOL_MAP = {
    "fetch_reddit_posts": fetch_reddit_posts,
    "fetch_news_articles": fetch_news_articles,
    "fetch_yahoo_finance_data": fetch_yahoo_finance_data,
    "fetch_twitter_finance_posts": fetch_twitter_finance_posts
}

class CustomFinAgent:
    def __init__(self):
        openai_api_key = st.secrets.get("OPENAI_API_KEY")
        if not openai_api_key:
            st.error("Missing OPENAI_API_KEY in secrets.")
        
        self.client = OpenAI(api_key=openai_api_key)

    def run(self, prompt, callbacks=None):
        # Initial Message
        messages = [
            {"role": "system", "content": "You are FinFriend. Use tools to fetch real-time data. Always summarize the data you find."},
            {"role": "user", "content": prompt}
        ]
        
        # 1. First Call
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )
        except Exception as e:
            return {"output": f"Error calling OpenAI: {e}"}

        msg = response.choices[0].message
        messages.append(msg)

        # 2. Check for Tool Call
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                if callbacks:
                    st.write(f"🔄 Creating `{tool_name}` with `{tool_args}`...")

                # Execute
                tool_func = TOOL_MAP.get(tool_name)
                tool_output_str = ""
                if tool_func:
                    try:
                        tool_output = tool_func(**tool_args)
                        tool_output_str = str(tool_output)
                    except Exception as e:
                        tool_output_str = f"Error: {e}"
                else:
                    tool_output_str = "Error: Tool not found."

                # Append Result
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output_str
                })
            
            # 3. Final Answer
            final_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            return {"output": final_response.choices[0].message.content}
        
        return {"output": msg.content}

def get_chat_engine():
    return CustomFinAgent()
