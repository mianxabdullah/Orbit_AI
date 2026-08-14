import streamlit as st
from chat_manager import create_chat

st.set_page_config(
    page_title="Orbit",
    page_icon="🪐",
    layout="wide"
)

st.title("Orbit")

# INITIALIZE
if "current_chat" not in st.session_state:
    st.session_state.current_chat = create_chat()

