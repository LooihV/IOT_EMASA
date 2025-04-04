FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles

# Ejecuta collectstatic antes de iniciar el servidor
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && python manage.py shell < init_superuser.py && daphne -b 0.0.0.0 -p 8000 drf.asgi:application"]