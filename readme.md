# Self-Service Database Server for Northwestern Medicine

Author: Tiger Nie [nhl0819@gmail.com]

Version: 1.0.0

Python >= 3.5

## Status

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/haolinnie/Self-Service-Database-Server/blob/master/LICENSE)
[![Build Status](https://travis-ci.com/haolinnie/Self-Service-Database-Mock-Server.svg?branch=master)](https://travis-ci.com/haolinnie/Self-Service-Database-Mock-Server)

## Documentation

[Here](https://tigernie.com/ssd_api) is the most up-to-date API documentation.

This app is built in Python 3 with the Flask microframework, and Gunicorn is the current production WSGI server of choice, although many others will also get the job done.


## Deployment steps

Clone the repo (working on easier deployment)

```bash
git clone https://github.com/haolinnie/Self-Service-Database-Mock-Server.git
cd Self-Service-Database-Mock-Server
```

Create & activate virtual environment

```bash
python3 -m venv flask
source flask/bin/activate
```

Install module

```
pip3 install --upgrade pip
pip3 install .
```

Start the server

```bash
chmod a+x deploy.sh
./deploy.sh
```

For deployment for production on a linux server, consider using `systemd` to configure the app as a daemon.


## Todo

Add more API features like searching for a specific entry in a column, and returning relevant data of those patients from other tables

Streamline the deployment process with Docker
