FROM python:3-slim

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

RUN adduser --disabled-password appuser && \
    chown -R appuser:appuser /app

USER appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off

EXPOSE 8000

CMD ["gunicorn"]
