import streamlit as st
from chat_manager import create_chat, load_chat, list_chats

def render_sidebar():
    
    with st.sidebar:
        st.title("⚙️ Settings")

        if st.button("New Chat", use_container_width=True):
            st.session_state.current_chat = create_chat()
            data = load_chat(st.session_state.current_chat)
            st.session_state.messages = data["messages"]
            st.rerun()

        # Search
        search = st.text_input("Recents", placeholder="Search...")

        # Chats
        chats = [chat for chat in list_chats() if chat["title"] != "New Chat"]

        if search:
            chats = [chat for chat in chats if search.lower() in chat["title"].lower()] 

        for chat in chats:
            col1, col2 = st.columns([9, 1])

            # Chat button
            with col1:
                active = chat["id"] == st.session_state.current_chat
                label = "🟢 " if active else ""
                
                if st.button(
                    label + chat["title"],
                    key=chat["id"],
                    use_container_width=True,
                ):
                    st.session_state.current_chat = chat["id"]
                    st.session_state.messages = chat["messages"]
                    st.rerun()