FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service ./service
COPY wsgi.py ./wsgi.py

# Create a non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 8080

# Use gunicorn in container
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]
