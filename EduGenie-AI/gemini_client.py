import json
from typing import Any

from config import GEMINI_API_KEY, GEMINI_MODEL


_client = None


class AIConfigurationError(RuntimeError):
    pass


class AIServiceError(RuntimeError):
    pass


def _load_sdk():

    try:
        from google import genai
        from google.genai import types

        return genai, types

    except ImportError as exc:

        raise AIConfigurationError(
            "google-genai is not installed. "
            "Run: pip install -r requirements.txt"
        ) from exc


def get_client():

    global _client

    genai, _ = _load_sdk()

    if not GEMINI_API_KEY:

        raise AIConfigurationError(
            "GEMINI_API_KEY is missing. "
            "Create a .env file and add your Gemini API key."
        )

    if _client is None:

        try:

            _client = genai.Client(
                api_key=GEMINI_API_KEY
            )

        except Exception as exc:

            raise AIServiceError(
                f"Could not initialize Gemini: {exc}"
            ) from exc

    return _client


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = 1200,
) -> str:

    client = get_client()

    _, types = _load_sdk()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config,
        )

    except Exception as exc:

        raise AIServiceError(
            f"Gemini request failed: {exc}"
        ) from exc

    text = getattr(
        response,
        "text",
        None
    )

    if not text or not text.strip():

        raise AIServiceError(
            "Gemini returned an empty response."
        )

    return text.strip()


def generate_json(
    prompt: str,
    *,
    max_output_tokens: int = 2200
) -> Any:

    client = get_client()

    _, types = _load_sdk()

    config = types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=max_output_tokens,
        response_mime_type="application/json",
        system_instruction=(
            "Return only valid JSON. "
            "Do not add Markdown or commentary."
        ),
    )

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config,
        )

    except Exception as exc:

        raise AIServiceError(
            f"Gemini request failed: {exc}"
        ) from exc

    raw = getattr(
        response,
        "text",
        None
    )

    if not raw:

        raise AIServiceError(
            "Gemini returned an empty JSON response."
        )

    try:

        return json.loads(raw)

    except json.JSONDecodeError:

        cleaned = (
            raw
            .strip()
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            return json.loads(cleaned)

        except json.JSONDecodeError as exc:

            raise AIServiceError(
                "Gemini returned invalid JSON."
            ) from exc