# 🪐 Orbit AI

A ChatGPT-style chatbot built with Streamlit and Groq, featuring streaming responses, chat history, document Q&A, and persistent storage via Supabase.

## Features

- 💬 Streaming chat responses (Groq API)
- 📂 Multiple chats with search, pin, rename, and delete (with confirmation)
- 📄 Upload a PDF, DOCX, or TXT file and ask questions about it
- 🏷️ Automatic AI-generated chat titles
- 🗄️ Persistent storage via Supabase (Postgres)
- 🎛️ Model selection (switch between Groq models)

## Tech Stack

- **Frontend/App:** Streamlit
- **LLM:** Groq API
- **Database:** Supabase (Postgres)
- **File parsing:** pypdf, python-docx

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/orbit-ai.git
   cd orbit-ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a Supabase project and run this SQL in the SQL Editor:
   ```sql
   create table chats (
     id text primary key,
     title text default 'New Chat',
     pinned boolean default false,
     document_name text default '',
     document_text text default '',
     model text,
     created_at timestamptz default now(),
     updated_at timestamptz default now(),
     messages jsonb default '[]'
   );

   alter table chats enable row level security;

   create policy "Allow all access"
   on chats
   for all
   using (true)
   with check (true);
   ```

4. Create `.streamlit/secrets.toml` in the project root:
   ```toml
   GROQ_API_KEY = "your-groq-api-key"
   SUPABASE_URL = "your-supabase-project-url"
   SUPABASE_KEY = "your-supabase-anon-key"
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Notes

- This is a single-user demo project — the Supabase `anon` key has open read/write access to the `chats` table (no per-user auth). Not intended for multi-tenant production use.
- On free hosting tiers with ephemeral storage, chat history persists via Supabase regardless of app restarts.

## Live Demo

[Add your Streamlit Cloud link here]