def build_prompt(english_text: str) -> str:
    return f"""Translate the following English text into Vietnamese.
Translate EXACTLY. Do not add or remove meaning.
Do not add greetings or explanations.

English:
{english_text}

Vietnamese:
"""
