FROM python:3.13.2-alpine

RUN adduser -D nonroot && \
    mkdir /app && \
    chown -R nonroot:nonroot /app

WORKDIR /app
USER nonroot

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    VIRTUAL_ENV=/app/.venv \
    GUNICORN_CMD_ARGS=--workers=3 --timeout=60 --bind=0.0.0.0:8000

COPY --chown=nonroot:nonroot . .

RUN pip install --upgrade pip
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app"]
