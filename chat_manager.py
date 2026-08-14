import uuid
import streamlit as st
from datetime import datetime, timezone
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"],
)


