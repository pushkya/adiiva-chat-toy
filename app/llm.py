import os
import json
import httpx
import asyncio

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
    provider = os.getenv("LLM_PROVIDER", "llama").lower()

    prompt = (
        "You are a friendly assistant talking to a child aged 4-8. "
        "Answer simply and kindly, avoiding unsafe or scary topics.\n\n"
        f"Question: {question}"
    )

    if provider == "openai":
        try:
            from openai import OpenAI
        except ImportError:
            return "OpenAI SDK is not installed."

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            return "OpenAI API key is not set."

        client = OpenAI(api_key=openai_api_key)
        try:
            # OpenAI client currently sync, run in executor for async compatibility
            loop = asyncio.get_event_loop()
            completion = await loop.run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                    max_tokens=128,
                )
            )
            answer = completion.choices[0].message.content
            return answer.strip()
        except Exception as e:
            return f"OpenAI API error: {e}"

    elif provider == "llama":
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        payload = {
            "model": "llama2:7b-chat",
            "prompt": prompt,
            "options": {"temperature": 0.6, "num_predict": 128},
        }

        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.post(ollama_url, json=payload)
                raw_text = response.text
                full_answer = await parse_ollama_response_async(raw_text)
                return full_answer
            except Exception as e:
                return f"Error contacting Llama backend: {e}"

    else:
        return f"Unsupported LLM provider: {provider}"
