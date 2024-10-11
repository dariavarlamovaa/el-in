FROM python:3.11.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /finnhike

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc postgresql-client

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .