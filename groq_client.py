from groq import Groq
import streamlit as st

API = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=API)

def stream_response(messages, model):

    return client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )