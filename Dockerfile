FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8501

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY sportrx ./sportrx
COPY evidence ./evidence
COPY docs/research ./docs/research
COPY examples ./examples
COPY scripts ./scripts

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ".[app]"

EXPOSE 8501

CMD ["sh", "-c", "python -m streamlit run app/streamlit_app.py --server.address 0.0.0.0 --server.port ${PORT} --server.headless true --browser.gatherUsageStats false"]
