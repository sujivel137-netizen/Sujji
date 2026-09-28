import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()


EXPLANATION_PROVIDER = os.getenv(
    "EXPLANATION_PROVIDER",
    "gemini"
).strip().lower()


LOCAL_EXPLANATION_MODEL = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
).strip()


MAX_INPUT_CHARS = int(
    os.getenv(
        "MAX_INPUT_CHARS",
        "20000"
    )
)