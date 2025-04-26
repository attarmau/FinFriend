# app/main.py

import streamlit as st
from app.chat_engine import get_chat_engine

st.set_page_config(page_title="FinFriend 💰", layout="centered")
st.title("🤖 FinFriend: Your Financial Chatbot")

user_input = st.text_input("Ask me anything about the market:")
if user_input:
    engine = get_chat_engine()
    response = engine.run(user_input)
    st.markdown(f"**FinFriend:** {response}")
