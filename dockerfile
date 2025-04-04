FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos necesarios
COPY requirements.txt .
COPY traductor.py .
COPY translate-en_es-1_0.argosmodel /root/.local/share/argos-translate/packages/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "traductor.py"]