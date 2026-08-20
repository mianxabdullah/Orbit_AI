import streamlit as st
from chat_manager import create_chat, load_chat, save_chat
from groq_client import stream_response
from config import SYSTEM_PROMPT
from sidebar import render_sidebar
from file_handler import extract_text

st.set_page_config(page_title="Orbit", page_icon="🪐", layout="wide")

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
    if (
        chat_data["document_name"] != uploaded_file.name
    ):  # check if the uploaded file is different from the previous one
        chat_data["document_name"] = uploaded_file.name
        chat_data["document_text"] = extract_text(uploaded_file)
        save_chat(st.session_state.current_chat, chat_data)

        # reload updated chat
        chat_data = load_chat(st.session_state.current_chat)

document_text = chat_data["document_text"]
st.sidebar.caption(f"Doc length: {len(document_text) if document_text else 0} chars")

if chat_data["document_name"]:
    st.sidebar.success(f"📄 {chat_data['document_name']}")

# DISPLAY CHAT
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# CHAT INPUT

# Read chat_input first so we know this run whether a message is being submitted or not. This is important because we only want to show suggestions when no message is being submitted.
user_input = st.chat_input("Type your message...")

if (
    "suggested_prompt" in st.session_state
):  # check if the suggested_prompt is in the session state
    user_input = st.session_state.pop("suggested_prompt")

# Only show suggestions if there's no message yet AND we're not
# currently processing a new one (button click or chat_input submit)
if len(st.session_state.messages) == 1 and not user_input:
    st.markdown("### 💡 Try asking")

    suggestions = [
        "Explain quantum computing simply.",
        "Summarize this document.",
        "Write a Python function.",
        "Plan a 7-day trip.",
    ]

    cols = st.columns(2)

    for i, prompt in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(prompt, use_container_width=True):
                st.session_state.suggested_prompt = prompt
                st.rerun()

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    chat_data = load_chat(
        st.session_state.current_chat
    )  # load the chat data from the database
    chat_data["messages"] = (
        st.session_state.messages
    )  # update the messages in the chat data with the new messages from the session state
    save_chat(
        st.session_state.current_chat, chat_data
    )  # save the updated chat data back to the database

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        reply = ""

    messages = st.session_state.messages.copy()

    if document_text: # if there's a document uploaded, insert a system message with the document text at index 1 (after the user's message)
        messages.insert(1,
            {
                "role": "system",
                "content": f"""
                                The user uploaded the following document.
                                Use it to answer their questions.
                                Document:{document_text}
                            """,
            })

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
