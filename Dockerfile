# Dockerfile

FROM python:3.9-slim

WORKDIR /adiiva-chat-toy
COPY / ./
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV LLM_PROVIDER=huggingface
ENV OLLAMA_URL=http://host.docker.internal:11434/api/generate

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]