# imagen base Python
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python","sh", "bash","-c","manage.py", "runserver", "0.0.0.0:8000", "python manage.py createsu && python manage.py collectstatic --no-input && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 drf.asgi:application"]