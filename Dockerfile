FROM python:3.10

# Установим системные зависимости для сборки pyswisseph
RUN apt-get update && apt-get install -y gcc pkg-config

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
