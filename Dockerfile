FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY docs ./docs

RUN mkdir -p /app/vector_store/faiss_index /app/knowledge_base

ENV INDEX_PATH=/app/vector_store/faiss_index
ENV OPENAI_MODEL=gpt-4o-mini

EXPOSE 8000
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]