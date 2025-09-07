import os
from huggingface_hub import InferenceClient

# Initialize InferenceClient once globally
HF_MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN environment variable not set.")

client = InferenceClient(HF_MODEL_ID, token=HF_API_TOKEN)

def generate_response(question: str) -> str:
    base_prompt = (
        "You are a very kind, gentle, and patient AI assistant talking to a child aged 4 to 8 years old. "
        "Your responses should be simple, friendly, empathetic, and easy for a young child to understand. "
        "Always speak in a positive and encouraging way, using simple words. "
        "Avoid any scary, complex, or unsafe topics. "
        "If the child asks about something unsafe or difficult, gently explain why it’s not okay to talk about that and offer a comforting or happy alternative topic instead. "
        "Be nurturing and caring, almost like a loving friend or teacher.\n\n"
        f"Respond to the following question kindly and simply:\n"
        f"Question: {question}"
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": base_prompt},
                {"role": "user", "content": f"Question: {question}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip() if response.choices else ""
        return answer if answer else "Sorry, I could not generate a response."
    except Exception as e:
        return f"Hugging Face Inference API error: {e}"