FROM python:3.5
MAINTAINER Tiger Nie nhl0819@gmail.com
RUN mkdir ssd_server
COPY . ssd_server
RUN pip install .
EXPOSE 5100

WORKDIR ssd_server
ENTRYPOINT ["gunicorn", "-w", "2", "--bind=127.0.0.1:5100", "app:app"]
