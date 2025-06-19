FROM python:3.11-slim

# Устанавливаем system зависимости и Rust вручную
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --only-binary=:all: --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
