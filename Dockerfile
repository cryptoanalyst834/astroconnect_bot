# Используем официальный Python 3.11
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY . .

# Установка зависимостей только из бинарников
RUN pip install --upgrade pip \
 && pip install --only-binary=:all: -r requirements.txt

# Запуск приложения
CMD ["python", "main.py"]
