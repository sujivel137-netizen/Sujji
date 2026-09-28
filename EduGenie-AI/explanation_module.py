from config import (
    EXPLANATION_PROVIDER,
    LOCAL_EXPLANATION_MODEL
)

from gemini_client import generate_text


_local_pipeline = None


def _local_explain(text: str) -> str:

    global _local_pipeline

    try:

        from transformers import pipeline

    except ImportError as exc:

        raise RuntimeError(
            "Local explanation needs transformers, torch "
            "and sentencepiece. "
            "Install requirements-local.txt first."
        ) from exc

    if _local_pipeline is None:

        _local_pipeline = pipeline(
            "text2text-generation",
            model=LOCAL_EXPLANATION_MODEL,
            tokenizer=LOCAL_EXPLANATION_MODEL,
        )

    prompt = (
        "Explain the following educational concept "
        "in very simple language. "
        "Use short sentences and one small example.\n\n"
        f"Concept: {text}"
    )

    result = _local_pipeline(
        prompt,
        max_new_tokens=220,
        do_sample=False
    )

    return result[0]["generated_text"].strip()


def explain_concept(text: str) -> str:

    if EXPLANATION_PROVIDER == "local":

        return _local_explain(text)

    prompt = f"""
Explain this concept for a beginner.

Requirements:

1. Give a one-sentence meaning.
2. Explain it in 3-5 simple points.
3. Give one easy real-world or academic example.
4. Avoid unnecessary jargon.

Concept:

{text}
""".strip()

    return generate_text(

        prompt,

        system_instruction=(
            "You are EduGenie. "
            "Teach difficult concepts in simple language."
        ),

        temperature=0.25,

        max_output_tokens=1000,
    )