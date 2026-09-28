from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import MAX_INPUT_CHARS
from explanation_module import explain_concept
from gemini_client import AIConfigurationError, AIServiceError
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Generative AI educational assistant",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


class QARequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=MAX_INPUT_CHARS
    )


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=MAX_INPUT_CHARS
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=MAX_INPUT_CHARS
    )

    count: int = Field(
        default=5,
        ge=1,
        le=10
    )


class LearnRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    level: str = Field(
        default="beginner",
        min_length=1,
        max_length=50
    )


def run_ai(function, *args):

    try:
        return function(*args)

    except (AIConfigurationError, AIServiceError) as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {exc}"
        ) from exc


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


@app.post("/qa")
def qa(payload: QARequest):

    return {
        "answer": run_ai(
            answer_question,
            payload.question
        )
    }


@app.post("/explain")
def explain(payload: TextRequest):

    return {
        "explanation": run_ai(
            explain_concept,
            payload.text
        )
    }


@app.post("/quiz")
def quiz(payload: QuizRequest):

    return {
        "quiz": run_ai(
            generate_quiz,
            payload.text,
            payload.count
        )
    }


@app.post("/summarize")
def summarize(payload: TextRequest):

    return {
        "summary": run_ai(
            summarize_text,
            payload.text
        )
    }


@app.post("/learn/recommendations")
def learning_path(payload: LearnRequest):

    return {
        "recommendations": run_ai(
            get_learning_recommendations,
            payload.topic,
            payload.level
        )
    }