from gemini_client import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following educational text
for quick revision.

Requirements:

- Keep the important facts.
- Remove repetition.
- Use simple language.
- Prefer 5-8 bullet points.
- Do not add information that is not in the text.

Text:

{text}
""".strip()

    return generate_text(

        prompt,

        system_instruction=(
            "You are an educational "
            "summarization assistant."
        ),

        temperature=0.2,

        max_output_tokens=1200,
    )