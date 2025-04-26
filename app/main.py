# from dotenv import load_dotenv
# load_dotenv()

import streamlit as st
from app.chat_engine import get_chat_engine

st.set_page_config(page_title="FinFriend 💰", layout="centered")
st.title("🤖 FinFriend: Your Financial Chatbot")

# 1. Chat history using session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. User input with placeholder
user_input = st.text_input(
    "Ask me anything about the market:",
    placeholder="e.g., What's happening in the stock market today?"
)

# 3. If there's input, run the chat engine and save to history
if user_input:
    with st.spinner("Thinking..."):
        try:
            engine = get_chat_engine()
            response = engine.run(user_input)

            # Append to chat history
            st.session_state.messages.append(("You", user_input))
            st.session_state.messages.append(("FinFriend", response))
        except Exception as e:
            st.error(f"Sorry, something went wrong: {e}")

# 4. Display chat history
if st.session_state.messages:
    st.markdown("### 💬 Chat History")
    for sender, message in st.session_state.messages:
        if sender == "You":
            st.markdown(f"**🧑 {sender}:** {message}")
        else:
            st.markdown(f"**🤖 {sender}:** {message}")
