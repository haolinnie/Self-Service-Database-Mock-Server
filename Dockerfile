FROM python:3.7-slim-buster
LABEL maintainer="nhl0819@gmail.com"

RUN mkdir server_instance
COPY . server_instance
RUN pip install server_instance/
EXPOSE 5100/tcp

ENTRYPOINT ["gunicorn", "-w", "2", "--bind=0.0.0.0:5100"]
CMD ["api:create_app(host='localhost', username='test_user', password='password', db_name='ssd_sample_database')"]

