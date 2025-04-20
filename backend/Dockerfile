FROM python:3.11-slim
# gcc & friends for building hnswlib inline
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential g++ && \
    rm -rf /var/lib/apt/lists/*

# ---- system libs for native wheels ----
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir \
    cassandra-driver==3.29.0 \
    numpy==1.26.4 \
    fastapi==0.110.0 \
    uvicorn==0.29.0 \
    pydantic \
    python-dotenv==1.0.1 \
    httpx==0.27.0 \
    openai==0.28.1 \
    PyJWT==2.8.0 \
    prometheus-client==0.20.0 \
    mypy==1.10.0 \
    slowapi==0.1.8 \
    redis==5.0.3 \
    hnswlib==0.8.0
COPY app .
COPY tests tests/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]