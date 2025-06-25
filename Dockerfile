FROM python:3.10-slim

# Системные зависимости для сборки flatlib/pyswisseph
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential pkg-config \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway проксирует порт автоматически, но для локального отладки:
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
