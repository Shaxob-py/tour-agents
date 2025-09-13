FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY ./ /app
RUN uv sync

CMD ["uv", "run", "python3", "main.py", "runserver", "0:8000"]