import os
import re

# Simple keyword filter, can replace or extend with OpenAI moderation API
UNSAFE_KEYWORDS = ["kill", "blood", "gun", "sex", "drugs", "abuse", "violence", "scary", "hurt", "weapon", "suicide"]

def is_safe_prompt(question: str) -> bool:
    # Lowercase and basic regex tokenization
    q = question.lower()
    for kw in UNSAFE_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", q):
            return False
    # Optional: Use OpenAI Moderation API if API key present
    openai_mod_key = os.getenv("OPENAI_API_KEY")
    if openai_mod_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_mod_key)
            mod = client.moderations.create(input=question)
            if any(mod.results.categories.values()):
                return False
        except Exception:
            pass
    return True
