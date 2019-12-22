FROM python:3.7-slim-buster
LABEL maintainer="Tiger Nie <nhl0819@gmail.com>"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

ENV FLASK_ENV=prod

EXPOSE 5100/tcp
ENTRYPOINT ["gunicorn", "-w", "2", "--bind=0.0.0.0:5100"]
CMD ["api:create_app(host='localhost', username='test_user', password='password', db_name='ssd_sample_database')"]

