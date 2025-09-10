# Usa un'immagine base con Python
FROM python:3.11-slim

# Imposta la working directory dentro il container
WORKDIR /app

# Copia solo requirements.txt per ottimizzare la cache dei layer
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del progetto
COPY . .

# Comando di default (puoi cambiarlo in docker-compose)
CMD ["python", "app.py"]
