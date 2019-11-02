FROM python:3.7-slim-buster

RUN adduser ssd_server

WORKDIR /home/ssd_server

COPY ssd_api ssd_api
COPY setup.py setup.py
COPY app.py app.py
COPY deploy.sh deploy.sh

RUN python -m venv flask
RUN flask/bin/pip install --upgrade pip
RUN flask/bin/pip install .
RUN flask/bin/pip install gunicorn

RUN chmod +x deploy.sh

RUN chown -R ssd_server:ssd_server ./
USER ssd_server

EXPOSE 5100
ENTRYPOINT ["./deploy.sh"]
