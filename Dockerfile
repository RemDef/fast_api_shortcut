FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 7995

#CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn main:app
#--host 0.0.0.0 --port 7995"]
CMD ["sh", "-c", "uv run alembic upgrade head && uv run gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:7995 --workers 4"]