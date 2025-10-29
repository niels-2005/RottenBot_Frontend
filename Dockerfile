FROM python:3.11-slim 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/ 

COPY pyproject.toml .
COPY uv.lock . 

COPY . /app 

WORKDIR /app

RUN uv sync --locked 

CMD ["streamlit", "run", "/app/src/rottenbot_frontend/app.py"]
