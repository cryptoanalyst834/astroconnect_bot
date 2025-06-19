FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Создание рабочей директории
WORKDIR /app

# Копирование файлов
COPY . /app

# Установка зависимостей Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска
CMD ["python", "main.py"]
