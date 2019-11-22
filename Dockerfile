FROM python:3.7-slim-buster

RUN adduser admin_user

WORKDIR /home/admin_user

COPY ssd_api ssd_api
COPY setup.py setup.py
COPY deploy.sh deploy.sh

RUN python -m venv flask
RUN flask/bin/pip install --upgrade pip
RUN flask/bin/pip install .
RUN flask/bin/pip install gunicorn

RUN chmod +x deploy.sh

RUN chown -R admin_user:admin_user ./
USER admin_user

EXPOSE 5100
ENTRYPOINT ["./deploy.sh"]
