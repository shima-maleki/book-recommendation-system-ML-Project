# syntax=docker/dockerfile:1

# Use uv-managed Python base image
FROM ghcr.io/astral-sh/uv:python3.11-bookworm AS base

WORKDIR /app

# Keep bytecode out of the image and make logs unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy

# System deps for scientific stack
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc gfortran libopenblas-dev liblapack-dev && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies with uv (uses pyproject + uv.lock)
COPY pyproject.toml uv.lock requirements.txt ./
RUN uv sync --frozen

# Copy project code and data
COPY src ./src
COPY Data ./Data
COPY artifacts ./artifacts
COPY notebooks ./notebooks
COPY README.md .

# Activate project venv for all commands
ENV PATH="/app/.venv/bin:${PATH}"

# Persist artifacts outside the container FS
VOLUME ["/app/artifacts"]

# Default command: retrain pipeline (override at runtime for prediction)
CMD ["uv", "run", "python", "-m", "src.pipelines.training_pipeline"]
