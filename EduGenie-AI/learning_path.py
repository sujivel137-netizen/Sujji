from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner"
) -> str:

    prompt = f"""
Create a personalized learning path
for the topic "{topic}".

Learner level: {level}

Use this structure:

1. Goal
2. Stage 1 - Foundations
3. Stage 2 - Core concepts
4. Stage 3 - Practice/projects
5. Stage 4 - Advanced topics
6. Suggested weekly timeline
7. Practice strategy
8. Resource types to search for

Keep it realistic, clear,
and beginner-friendly.

Do not invent specific URLs.
""".strip()

    return generate_text(

        prompt,

        system_instruction=(
            "You are a study-plan designer. "
            "Make learning paths structured "
            "and achievable."
        ),

        temperature=0.35,

        max_output_tokens=1600,
    )