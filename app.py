import streamlit as st
from chat_manager import create_chat,load_chat,save_chat
from groq_client import stream_response
from config import SYSTEM_PROMPT,DEFAULT_MODEL as model

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
 
    chat_data = load_chat(st.session_state.current_chat) # load the chat data from the database
    chat_data["messages"] = st.session_state.messages # update the messages in the chat data with the new messages from the session state
    save_chat(st.session_state.current_chat, chat_data) # save the updated chat data back to the database

    with st.chat_message("user"): 
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        reply = ""

    messages = st.session_state.messages.copy() 

    try:
        response = stream_response(messages, model)

        for chunk in response:
            text = chunk.choices[0].delta.content
            if text:
                reply += text
                placeholder.markdown(reply)

    except Exception as e:
        placeholder.error(f"Something went wrong: {e}")
        reply = None
