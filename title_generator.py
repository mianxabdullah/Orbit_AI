from groq_client import client
from config import DEFAULT_MODEL

def generate_title(first_message):
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You generate short chat titles. "
                    "You will be given a user's message. "
                    "Do not answer or respond to it — only summarize "
                    "its topic in 3-5 words with maximum 15 characters. Return ONLY the title, "
                    "no punctuation, no quotes."
                ),
            },
            {
                "role": "user",
                "content": f"Message to title: {first_message}",
            },
        ],
    )

    title = response.choices[0].message.content.strip() 
    if len(title) > 12:
        return title[:12] + "..."  # hard safety cap
    return title 