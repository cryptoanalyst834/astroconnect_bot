# Базовый образ с Python 3.11 и Rust (через rustlang)
FROM python:3.11-slim

# Установка зависимостей ОС и Rust toolchain
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libpq-dev \
    curl \
    build-essential \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . "$HOME/.cargo/env"

# Установка poetry/maturin при необходимости
ENV PATH="/root/.cargo/bin:$PATH"

# Создание директории проекта
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Установка зависимостей (используется Rust через maturin при необходимости)
RUN pip install --upgrade pip \
    && pip install wheel \
    && pip install -r requirements.txt

# Копируем остальной код проекта
COPY . .

# Открываем порт (если нужно для webhook)
EXPOSE 8080

# Запуск твоего бота (замени main.py на свою точку входа)
CMD ["python", "main.py"]
