FROM python:3.12.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    netcat-openbsd \
    postgresql-client


WORKDIR /app/

COPY requirements/dev.txt requirements/prod.txt ./

RUN python -m pip install --upgrade pip --no-warn-script-location && \
    pip install -r dev.txt --no-cache-dir --no-warn-script-location && \
    pip install -r prod.txt --no-cache-dir --no-warn-script-location

COPY . .

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]