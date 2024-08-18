# Stage 1: Build stage
FROM python:3.9-slim AS build

WORKDIR /app

COPY requirements.txt .
RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

COPY src .

FROM python:3.9-slim

COPY --from=build /app /app
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app/

ENTRYPOINT ["celery", "-A", "main", "worker", "--loglevel=INFO"]