FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar utilitários e compiladores para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar pacotes Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código-fonte
COPY . .

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8001"]
