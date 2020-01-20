# Self-Service Database Server for Northwestern Medicine

[![Build Status](https://travis-ci.com/haolinnie/Self-Service-Database-Server.svg?branch=master)](https://travis-ci.com/haolinnie/Self-Service-Database-Server)
[![Coverage Status](https://coveralls.io/repos/github/haolinnie/Self-Service-Database-Server/badge.svg)](https://coveralls.io/github/haolinnie/Self-Service-Database-Server)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/haolinnie/Self-Service-Database-Server/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/haolinnie/Self-Service-Database-Server/?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/cf924c7e3dd6dc57e4f3/maintainability)](https://codeclimate.com/github/haolinnie/Self-Service-Database-Server/maintainability)

Author: Tiger Nie [nhl0819@gmail.com]

Version: 1.1

This is the API server for a Self-Service Database UI for Northwestern Memorial Hospital's Ophthalmology department. The app is written in Python 3.7 with MySQL as the database layer. Currently deployable via a bash script with gunicorn and NGINX. Docker recipes are in the works.

## API Documentation

Please read the API documentation to understand the structure of the endpoints. A graphical debugger is available for quick experimentation with the API.

[API documentation.](docs/APIDocumentation.md)

[API debugger](https://tigernie.com/ssd_api)

## Getting Started

### Download the source code

```bash
git clone https://github.com/haolinnie/Self-Service-Database-Server.git
cd Self-Service-Database-Server
```

### Prerequisites

- Python 3.6+
- MariaDB 10.4.10 (or equivalent MySQL server)

### Setup a development environment

#### Create a sample MySQL database

A script will generate a test user with username: test_user and password: password, and generate the database schema along with 10 patients.

```bash
mysql < data/create_sample_database.sql
```

#### Create and activate virtual environment

```bash
python3 -m venv flask
source flask/bin/activate
```

#### Install python dependencies

```bash
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```

### Test the server

Start a development server

```bash
python3 debug.py
```

Start a production server

```bash
chmod a+x deploy.sh
./deploy.sh
```

## Deployment

A sample is deployed at https://tigernie.com/ssd_api

Docker is being worked on for a more streamlined deployment process.
