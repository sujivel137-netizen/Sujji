from gemini_client import generate_json


def _normalize_quiz(data, count: int):

    if isinstance(data, dict):

        data = data.get(
            "questions",
            data.get("quiz", [])
        )

    if not isinstance(data, list):

        raise RuntimeError(
            "Quiz response was not a list of questions."
        )

    result = []

    for item in data:

        if len(result) >= count:
            break

        if not isinstance(item, dict):
            continue

        question = str(
            item.get("question", "")
        ).strip()

        options = item.get(
            "options",
            []
        )

        answer = str(
            item.get(
                "correct_answer",
                item.get("answer", "")
            )
        ).strip()

        explanation = str(
            item.get(
                "explanation",
                ""
            )
        ).strip()

        if (
            question
            and isinstance(options, list)
            and len(options) == 4
            and answer
        ):

            options = [
                str(x).strip()
                for x in options
            ]

            if answer in options:

                result.append({
                    "question": question,
                    "options": options,
                    "correct_answer": answer,
                    "explanation": explanation
                })

    if len(result) < count:

        raise RuntimeError(
            "The AI did not return enough valid "
            "quiz questions. Try again."
        )

    return result


def generate_quiz(
    passage: str,
    count: int = 5
):

    prompt = f"""
Create exactly {count} multiple-choice questions
from the passage below.

Return this JSON shape:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "One option exactly as written",
      "explanation": "Short explanation"
    }}
  ]
}}

Rules:

- Every question must be answerable from the passage.
- Exactly four options per question.
- Only one correct answer.
- correct_answer must exactly match one option.
- Keep language student-friendly.

Passage:

{passage}
""".strip()

    data = generate_json(
        prompt
    )

    return _normalize_quiz(
        data,
        count
    )