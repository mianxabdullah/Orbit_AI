import streamlit as st
from chat_manager import create_chat,load_chat,save_chat
from groq_client import stream_response
from config import SYSTEM_PROMPT,DEFAULT_MODEL as model
from sidebar import render_sidebar
from file_handler import extract_text

st.set_page_config(
    page_title="Orbit",
    page_icon="🪐",
    layout="wide"
)

st.title("Orbit")

# used to remove the avatars from the chat messages
st.markdown(   
    """
<style>
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    display: none;
}
</style>
""",
    unsafe_allow_html=True,
)

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

# SIDEBAR
model, uploaded_file = render_sidebar()
chat_data = load_chat(st.session_state.current_chat)

if uploaded_file:
    if chat_data["document_name"] != uploaded_file.name: # check if the uploaded file is different from the previous one
        chat_data["document_name"] = uploaded_file.name
        chat_data["document_text"] = extract_text(uploaded_file)
        save_chat(st.session_state.current_chat, chat_data)

        # reload updated chat
        chat_data = load_chat(st.session_state.current_chat)

document_text = chat_data["document_text"] 

if chat_data["document_name"]:
    st.sidebar.success(f"📄 {chat_data['document_name']}")

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

    if reply:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )

        chat_data = load_chat(st.session_state.current_chat)
        chat_data["messages"] = st.session_state.messages
        save_chat(st.session_state.current_chat, chat_data)
