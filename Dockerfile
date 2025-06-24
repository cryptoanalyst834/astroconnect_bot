# Используем официальный Python-образ
FROM python:3.10-slim

# Устанавливаем gcc и зависимости для psycopg2 и flatlib
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Открываем порт (если нужно для FastAPI)
EXPOSE 8000

# Запускаем приложение
CMD ["python", "main.py"]
