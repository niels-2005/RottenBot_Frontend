FROM python:3.11-slim 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/ 

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock . 

RUN uv sync --locked 

COPY . /app 

EXPOSE 8501

ENV PYTHONPATH=/app

CMD ["uv", "run", "streamlit", "run", "src/rottenbot_frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
