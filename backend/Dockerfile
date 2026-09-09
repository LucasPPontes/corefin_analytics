FROM python:3.12-slim

WORKDIR /app

# Instalar dependências Python do Backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar arquivos do backend e os dados
COPY backend/ ./backend/
COPY data/ ./data/

EXPOSE 8001

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8001"]
