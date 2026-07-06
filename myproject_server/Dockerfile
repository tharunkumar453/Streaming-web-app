FROM python:3.12-slim

# Install system dependencies

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# Copy dependency files first
COPY ./pyproject.toml ./
# COPY uv.lock ./   # Uncomment if you have one

# Install dependencies
RUN uv sync --no-dev 

# Copy project
COPY . .

# Install project
RUN uv sync --no-dev

# Default command (can be overridden by Docker Compose)
CMD ["uv","run","python","manage.py","runserver","0.0.0.0:8000"]