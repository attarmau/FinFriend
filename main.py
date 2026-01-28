import streamlit as st
from app.chat_engine import get_chat_engine


st.set_page_config(page_title="FinFriend 💰", layout="centered")
st.title("🤖 FinFriend: Your Financial Chatbot")

# 1. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm FinFriend. I can check Reddit, News, Twitter, and Stock Prices for you. Ask me about a stock or the economy!"}
    ]

# 2. Display Chat History
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 3. Handle User Input
if prompt := st.chat_input(placeholder="What is the sentiment on Reddit about Tesla?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 4. Agent Response
    with st.chat_message("assistant"):
        try:
            agent = get_chat_engine()
            # Pass dummy list to trigger internal status updates
            response = agent.run(prompt, callbacks=[True])
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
            st.write(response["output"])
        except Exception as e:
            st.error(f"Error: {e}")
