FROM python:3.11.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app/

RUN apt-get update

COPY ./requirements.txt .
RUN pip install -r requirements.txt
