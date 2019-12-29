# Dockerfile for production
FROM python:3.7-slim-buster
LABEL maintainer="Tiger Nie <nhl0819@gmail.com>"

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY credentials.config /app/
COPY api /app/api

WORKDIR /app

#ENV FLASK_ENV=prod

EXPOSE 5100
ENTRYPOINT ["gunicorn", "-w", "2", "--bind=0.0.0.0:5100", "--log-level", "INFO", "api:create_app()"]
