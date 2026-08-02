FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml ./
# If you have one, copy the lock file too
# COPY uv.lock ./

# Install only dependencies
RUN uv sync --no-dev --no-install-project

# Copy application source
COPY . .

# Install the local project
RUN uv sync --no-dev

CMD ["uv", "run", "celery", "-A", "task.celery_app_instance", "worker", "-Q", "reels_processing_queue", "--loglevel=info"]