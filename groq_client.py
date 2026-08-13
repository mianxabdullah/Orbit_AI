from groq import Groq
import streamlit as st

API = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=API)

