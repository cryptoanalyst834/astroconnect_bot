FROM python:3.10-slim

# Устанавливаем все системные пакеты для сборки C-расширений
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      pkg-config \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Открываем порт
EXPOSE 8000

# Запускаем Uvicorn (FastAPI + background polling/webhook)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
