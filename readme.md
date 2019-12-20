# Self-Service Database Server for Northwestern Medicine

Author: Tiger Nie [nhl0819@gmail.com]

[![Build Status](https://travis-ci.com/haolinnie/Self-Service-Database-Server.svg?branch=master)](https://travis-ci.com/haolinnie/Self-Service-Database-Server)
[![Coverage Status](https://coveralls.io/repos/github/haolinnie/Self-Service-Database-Server/badge.svg?branch=master)](https://coveralls.io/github/haolinnie/Self-Service-Database-Server?branch=master)

This is the API server for a Self-Service Database UI for Northwestern Memorial Hospital's Ophthalmology department. The app is written in Python 3.7 with MySQL as the database layer. Currently deployable via a bash script with gunicorn and NGINX. Docker recipes are in the works.

## Documentation

[Here is the most up-to-date API documentation.](https://github.com/haolinnie/Self-Service-Database-Server/blob/master/ssd_api/APIDocumentation.md) 

[Here is a nice little API debugger for this project.](https://tigernie.com/ssd_api)


## Deployment steps

A Linux server is recommended. A MariaDB/MySQL Server must be connected.

Clone the repo (working on easier deployment with Docker containers)

```bash
git clone https://github.com/haolinnie/Self-Service-Database-Mock-Server.git
cd Self-Service-Database-Mock-Server
```

Create & activate virtual environment

```bash
python -m venv flask
source flask/bin/activate
```

Install the app factory module

```
python -m pip install --upgrade pip
python -m pip install .
```

Start the server

```bash
chmod a+x deploy.sh
./deploy.sh
```

For deployment on a linux server, consider using `systemd` to configure the app as a daemon before Dockers are ready.


## Todo

Add more API features to support the front end.
Streamline the deployment process with Docker.
