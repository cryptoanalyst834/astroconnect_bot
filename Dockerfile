FROM python:3.10-slim

# Системные зависимости для сборки C-расширений
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      pkg-config \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

# Открыть порт (необязательно — Railway сам проксирует)
EXPOSE 8000

# Важно: используем переменную $PORT от Railway
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
