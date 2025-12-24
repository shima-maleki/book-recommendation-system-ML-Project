"""FastAPI service for book recommendations."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.pipelines import prediction_pipeline

app = FastAPI(title="Book Recommendation API", version="0.1.0")


class RecommendationRequest(BaseModel):
    book: str = Field(..., description="Exact book title to query.")


class RecommendationResponse(BaseModel):
    book: str
    recommendations: list[str]
    poster_urls: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(payload: RecommendationRequest) -> RecommendationResponse:
    if not payload.book:
        raise HTTPException(status_code=400, detail="Book title must be provided.")
    try:
        recs, posters = prediction_pipeline.recommend_book(payload.book)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # broad to surface errors cleanly
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {exc}",
        ) from exc
    if not recs:
        raise HTTPException(
            status_code=404, detail=f"No recommendations found for '{payload.book}'."
        )
    return RecommendationResponse(
        book=payload.book, recommendations=recs, poster_urls=posters
    )
