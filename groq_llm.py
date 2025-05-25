import httpx
import os
from dotenv import load_dotenv
from utils import logger

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def explain_recommendations(prompt, items):
    if not items:
        return []
    
   
    system_prompt = (
    "You are an AI assistant that explains why a user's interest matches a list of items. "
    "For each item, write a one-sentence explanation that is directly related to the user's interest. "
    "Number each explanation to match the list. If an item is not relevant, say 'Not relevant'. "
    "Do not include any generic text like 'Here are the explanations'. Just list numbered explanations only."
)

    
    user_input = f"User interest: {prompt}\n\nItems:\n" + "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])
    
    try:
        response = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.5
            },
            timeout=60
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"]
        explanations = raw.split("\n")
        return [e.strip().split(". ", 1)[1] if ". " in e else e for e in explanations]
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return ["No explanation available."] * len(items)
