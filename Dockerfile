FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY ./ /app

RUN uv sync

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
