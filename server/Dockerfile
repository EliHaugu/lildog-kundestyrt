FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
EXPOSE 8765

# Run database migrations, start Django and WebSocket servers in parallel
CMD ["sh", "-c", "python server_comm/manage.py migrate && python server_comm/manage.py runserver 0.0.0.0:8000 & python server.py"]
