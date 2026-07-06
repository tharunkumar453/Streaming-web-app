FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for Docker layer caching)
COPY pyproject.toml ./

RUN uv sync --no-dev --no-install-project
# COPY uv.lock ./   # Uncomment if you have one



# Copy project
COPY . .

# Install project
RUN uv sync --no-dev

# Default command (can be overridden by Docker Compose)
CMD ["uv","run","python","manage.py","runserver","0.0.0.0:8000"]