import uuid
import streamlit as st
from datetime import datetime, timezone
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"],
)

def create_chat():
    chat_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    data = {
        "id": chat_id,
        "title": "New Chat",
        "pinned": False,
        "document_name": "",
        "document_text": "",
        "model": None,
        "created_at": now,
        "updated_at": now,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful chatbot."
            }
        ]
    }

    supabase.table("chats").insert(data).execute()
    return chat_id

def load_chat(chat_id):
    res = supabase.table("chats").select("*").eq("id", chat_id).single().execute()
    return res.data
