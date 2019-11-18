# Self-Service Database Server for Northwestern Medicine

Author: Tiger Nie [nhl0819@gmail.com]

Version: 1.0.0

Python >= 3.5

[![Build Status](https://travis-ci.com/haolinnie/Self-Service-Database-Server.svg?branch=master)](https://travis-ci.com/haolinnie/Self-Service-Database-Server)

## Documentation

[Here is the most up-to-date API documentation.](https://github.com/haolinnie/Self-Service-Database-Server/blob/master/ssd_api/APIDocumentation.md) 

This app is built in Python 3 with the Flask microframework, and Gunicorn is the current production WSGI server of choice, although many others will also get the job done.

A SQLite database is used for the current prototype. Work is being done to migrate to MariaDB (an open source fork of MySQL).


## Deployment steps

A Linux server is recommended, although MacOS is supported.

Clone the repo (working on easier deployment with Docker containers)

```bash
git clone https://github.com/haolinnie/Self-Service-Database-Mock-Server.git
cd Self-Service-Database-Mock-Server
```

Create & activate virtual environment

```bash
python3 -m venv flask
source flask/bin/activate
```

Install the app factory module

```
pip3 install --upgrade pip
pip3 install .
```

Start the server

```bash
chmod a+x deploy.sh
./deploy.sh
```

For deployment on a linux server, consider using `systemd` to configure the app as a daemon :)


## Todo

Add more API features to support the front end.
Streamline the deployment process with Docker.
Support external DB such as MariaDB and MySQL.
