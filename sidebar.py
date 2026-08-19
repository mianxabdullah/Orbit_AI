import streamlit as st
from chat_manager import create_chat, load_chat, list_chats, toggle_pin, delete_chat, rename_chat
from config import DEFAULT_MODEL

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

            # Three-dot menu
            with col2:
                with st.popover(""):
                    #Pin/Unpin button
                    pin_text = "📌 Unpin" if chat.get("pinned", False) else "Pin"

                    if st.button(
                        pin_text,
                        key=f"pin_{chat['id']}",
                        use_container_width=True,
                    ):
                        toggle_pin(chat["id"])
                        st.rerun()

                    # Delete button    
                    confirm_key = f"confirm_delete_{chat['id']}"

                    if not st.session_state.get(confirm_key):
                        if st.button("Delete", key=f"delete_{chat['id']}", use_container_width=True):
                            st.session_state[confirm_key] = True
                            st.rerun()
                    else:
                        st.write("Delete this chat?")
                        if st.button("Yes, delete", key=f"yes_{chat['id']}", use_container_width=True):
                            delete_chat(chat["id"])

                            if chat["id"] == st.session_state.current_chat:
                                st.session_state.current_chat = create_chat()
                                data = load_chat(st.session_state.current_chat)
                                st.session_state.messages = data["messages"]

                            st.session_state.pop(confirm_key, None)
                            st.rerun()

                    # Rename button
                    new_title = st.text_input(
                        "Rename Chat", value=chat["title"], key=f"title_{chat['id']}"
                    )

                    if st.button(
                        "Rename",
                        key=f"save_{chat['id']}",
                        use_container_width=True,
                    ):
                        rename_chat(chat["id"], new_title)
                        st.rerun()

        st.divider()

        # Model selection
        st.subheader("Model")
        model = st.selectbox(
            "Choose Model",
            [
                DEFAULT_MODEL,
                "qwen/qwen3.6-27b",
            ],
        )     

        return model     