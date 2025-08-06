FROM python:3.10-slim

# 1. Evita cache innecesaria en build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copia solo lo que necesitas
COPY main.py .
COPY payload_processing.py .
COPY websockets_server.py .
COPY health_check.py .  
# Si tienes módulos extra, copia el directorio:
# COPY src/ ./src/

# 3. Define un usuario no-root (opcional pero recomendable)
RUN addgroup --system appgroup && adduser --system --group appuser
USER appuser

# 4. CMD inmutable y logging mejor
CMD ["bash", "-c", "python main.py"]