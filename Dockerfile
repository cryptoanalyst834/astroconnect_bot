FROM python:3.10-slim

# Устанавливаем системные зависимости для сборки pyswisseph
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      gcc \
      pkg-config \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем Uvicorn (FastAPI + webhook/long polling внутри main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
