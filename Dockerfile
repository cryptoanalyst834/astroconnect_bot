FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential python3-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# ↓↓↓ ДОПОЛНИТЕЛЬНО, если проблемы с flatlib
RUN pip install flatlib==0.2.3

COPY . .

RUN find . -name '*.pyc' -delete

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
