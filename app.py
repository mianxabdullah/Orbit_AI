import streamlit as st
from chat_manager import create_chat,load_chat
from config import SYSTEM_PROMPT

st.set_page_config(
    page_title="Orbit",
    page_icon="🪐",
    layout="wide"
)

st.title("Orbit")

# INITIALIZE
if "current_chat" not in st.session_state:
    st.session_state.current_chat = create_chat()

if "messages" not in st.session_state:
    data = load_chat(st.session_state.current_chat)

    if data["messages"]:
        st.session_state.messages = data["messages"]
    else:
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

# DISPLAY CHAT 
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CHAT INPUT
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )
