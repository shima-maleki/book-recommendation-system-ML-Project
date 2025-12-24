# Book Recommendation System – Architecture

This document explains how the application is wired end to end: data flow, pipelines, services, artifacts, and how they are deployed with Docker + uv.

## Overview
- Goal: Item-based collaborative-filtering recommender that returns similar books for a given title.
- Core components:
  - Data ingestion pipeline (`src/pipelines/data_pipeline.py`)
  - Data preprocessing pipeline (`src/components/data_preprocessing.py`)
  - Model training pipeline (`src/components/model_preparation.py`)
  - Prediction pipeline (`src/pipelines/prediction_pipeline.py`)
  - FastAPI service (`app.py`)
  - Streamlit UI (`streamlit_app.py`)
  - Docker + Compose environment (uv-managed Python)
- Key artifacts (all under `artifacts/`): `books.csv`, `users.csv`, `ratings.csv`, `ratings.pkl`, `book_pivot.pkl`, `books_title.pkl` (or `books_name.pkl`), `model.pkl`.

### High-Level Data + Service Flow
```
          Raw CSVs (Data/)
                 |
          [Ingestion Pipeline]
                 |
          Clean CSVs (artifacts/)
                 |
          [Preprocessing Pipeline]
                 |
      ratings.pkl | book_pivot.pkl | books_title.pkl
                 |
          [Training Pipeline]
                 |
              model.pkl
                 |
    ┌─────────────────────────────┐
    │      Prediction Pipeline    │
    │ (loads model + pivot + meta)│
    └─────────────┬───────────────┘
                  |
          ┌───────┴────────┐
          │                │
   FastAPI (/recommend)    │
          │                │
          └───────► Streamlit UI
```

## Data Flow and Pipelines

### 1) Data ingestion (`src/pipelines/data_pipeline.py`)
- Reads raw CSVs from `Data/` (`books.csv`, `users.csv`, `ratings.csv`).
- Cleans book columns (drops year + small/medium images, renames to `title`, `author`, `publisher`, `url`).
- Renames ratings columns (`User-ID`→`user_id`, `Book-Rating`→`rating`).
- Saves cleaned copies to `artifacts/books.csv`, `artifacts/users.csv`, `artifacts/ratings.csv`.

### 2) Preprocessing (`src/components/data_preprocessing.py`)
- Input: cleaned CSVs (paths returned by ingestion).
- Filters active users (>200 ratings).
- Merges ratings with books on `ISBN`.
- Counts ratings per title and keeps titles with ≥50 ratings.
- Drops duplicate (title, user_id) rows.
- Builds user-book pivot (index=title, columns=user_id, values=rating_y) and fills NaNs with 0.
- Extracts `book_titles`.
- Saves: `artifacts/ratings.pkl`, `artifacts/book_pivot.pkl`, `artifacts/books_title.pkl`.

### 3) Model training (`src/components/model_preparation.py`)
- Loads `book_pivot.pkl`.
- Converts to sparse CSR matrix.
- Fits `NearestNeighbors` (brute-force) on the sparse matrix.
- Saves model to `artifacts/model.pkl`.

### 4) Prediction (`src/pipelines/prediction_pipeline.py`)
- Loads artifacts from `ARTIFACT_DIR` (default `artifacts/`); falls back to `books_name.pkl` if `books_title.pkl` absent.
- `recommend_book(title)`: finds the title row, retrieves nearest neighbors from the trained model, excludes the query title, and returns recommended titles plus poster URLs (when found in ratings).
- CLI entry: `python -m src.pipelines.prediction_pipeline --book "<title>"`.

#### Pipelines Interaction Diagram
```
data_pipeline.py
    └─> artifacts/books.csv
        artifacts/users.csv
        artifacts/ratings.csv
             |
data_preprocessing.py
    └─> artifacts/ratings.pkl
        artifacts/book_pivot.pkl
        artifacts/books_title.pkl
             |
model_preparation.py
    └─> artifacts/model.pkl
             |
prediction_pipeline.py
    └─> recommend_book(title)
```

## Services

### FastAPI (`app.py`)
- `/health`: liveness check.
- `/recommend`: POST `{"book": "<title>"}` → returns recommendations and poster URLs.
- Returns 404 when a title is not in the pivot; 500 for other errors.

### Streamlit UI (`streamlit_app.py`)
- Styled front end that calls the FastAPI endpoint.
- Default API URL: `http://localhost:18000/recommend` (configurable via `API_URL` env).
- Renders recommendations in card layout with optional cover URLs.

## Docker and Orchestration

### Dockerfile
- Base: `ghcr.io/astral-sh/uv:python3.11-bookworm`.
- Installs system libs for scientific stack, syncs deps via `uv sync`.
- Copies code, data, artifacts, notebooks, `app.py`, `streamlit_app.py`.
- Exposes `/app/artifacts` as a volume.
- Default CMD runs training pipeline (override in Compose).

### docker-compose.yml (key services)
- `data`: runs ingestion only.
- `train`: runs full training pipeline (ingestion + preprocessing + model).
- `predict`: runs CLI prediction (example book).
- `api`: runs FastAPI with uvicorn (mapped to host `18000:8000`).
- `ui`: runs Streamlit (mapped to host `18001:8501`), configured to hit `api`.
- Shared named volume: `artifacts` mounted at `/app/artifacts`; `./Data` mounted read-only where needed.

#### Compose Topology Diagram
```
           artifacts volume (shared)
          ┌───────────────────────┐
          │                       │
      ┌────────┐             ┌────────┐
      │ data   │             │ train  │
      └────┬───┘             └───┬────┘
          │                      │
          └────────────┬─────────┘
                       │
                 ┌─────▼──────┐
                 │   api      │  (FastAPI on 18000)
                 └─────┬──────┘
                       │
                 ┌─────▼──────┐
                 │    ui      │  (Streamlit on 18001)
                 └────────────┘
```

## Typical Runtime Sequence
1) Build images: `docker compose build`.
2) Generate artifacts: `docker compose run --rm train` (or `data` then `train`).
3) Serve: `docker compose up api ui`.
4) Query: use UI at http://localhost:18001 or curl API:  
   `curl -X POST http://localhost:18000/recommend -H "Content-Type: application/json" -d '{"book": "A Bend in the Road"}'`

## Error Handling and Edge Cases
- If a queried title is not in the pivot, prediction raises `ValueError`; API returns 404 with the message.
- Poster URL lookup logs a warning when a cover is missing and skips it.
- Missing `books_title.pkl` automatically falls back to `books_name.pkl` to match existing artifacts.

## Dev Notes
- Uses uv for dependency management; Python 3.11.
- Artifacts persist across container runs via the named volume; remove with `docker volume rm book-recommendation-system-ml-project_artifacts` for a clean slate.
- To adjust ports, update `docker-compose.yml` and the `API_URL` env for the UI if running outside Compose.
