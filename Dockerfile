FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app
COPY uv.lock pyproject.toml ./

RUN uv sync --no-cache

COPY .. .
CMD ["uv", "run", "app.py"]