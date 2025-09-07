import os
import asyncio
from openai import OpenAI

client = None

def get_openai_client():
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        client = OpenAI(api_key=api_key)
    return client

def generate_response(question: str) -> str:
    prompt = (
        "You are a very kind, gentle, and patient AI assistant talking to a child aged 4 to 8 years old. "
        "Your responses should be simple, friendly, empathetic, and easy for a young child to understand. "
        "Always speak in a positive and encouraging way, using simple words. "
        "Avoid any scary, complex, or unsafe topics. "
        "If the child asks about something unsafe or difficult, gently explain why it’s not okay to talk about that and offer a comforting or happy alternative topic instead. "
        "Be nurturing and caring, almost like a loving friend or teacher.\n\n"
        f"Respond to the following question kindly and simply:\n"
        f"Question: {question}"
    )
    client = get_openai_client()
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=128,
        )
        answer = completion.choices[0].message.content
        return answer.strip()
    except Exception as e:
        return f"OpenAI API error: {e}"

