from gemini_client import generate_text


def answer_question(question: str) -> str:

    prompt = f"""
You are EduGenie, a friendly educational assistant.

Answer the student's question accurately and clearly.

Rules:
- Start with the direct answer.
- Use simple language.
- Add a short example when useful.
- If the question is ambiguous, state the assumption.
- Do not invent facts.

Student question:

{question}
""".strip()

    return generate_text(

        prompt,

        system_instruction=(
            "You are a patient teacher. "
            "Prefer concise, student-friendly explanations."
        ),

        temperature=0.25,

        max_output_tokens=1000,
    )