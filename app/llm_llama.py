import os
import json
import httpx

async def parse_ollama_response_async(raw_response_text: str) -> str:
    lines = raw_response_text.strip().split("\n")
    full_response_parts = []
    for line in lines:
        try:
            data = json.loads(line)
            part = data.get("response", "")
            full_response_parts.append(part)
            if data.get("done", False):
                break
        except json.JSONDecodeError:
            continue
    full_response = "".join(full_response_parts).strip()
    return full_response if full_response else "Sorry, no answer available."


async def generate_response_async(question: str) -> str:
    ollama_url = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama2-chat-7b")
    prompt = (
        "You are a friendly assistant talking to a child aged 4-8. "
        "Answer simply and kindly, avoiding unsafe or scary topics.\n\n"
        f"Question: {question}"
    )
    payload = {
        "model": ollama_model,
        "prompt": prompt,
        "options": {"temperature": 0.6, "num_predict": 128},
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(ollama_url, json=payload)
            raw_text = response.text
            print("Raw LLaMA backend response:", raw_text)  # Debug print
            full_answer = await parse_ollama_response_async(raw_text)
            print("Parsed full answer:", full_answer)  # Debug print
            return full_answer
        except Exception as e:
            return f"Error contacting Llama backend: {e}"