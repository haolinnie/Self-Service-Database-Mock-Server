# Self-Service Database Server for Northwestern Medicine

[![Build Status](https://travis-ci.com/haolinnie/Self-Service-Database-Server.svg?branch=master)](https://travis-ci.com/haolinnie/Self-Service-Database-Server)
[![Coverage Status](https://coveralls.io/repos/github/haolinnie/Self-Service-Database-Server/badge.svg)](https://coveralls.io/github/haolinnie/Self-Service-Database-Server)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/haolinnie/Self-Service-Database-Server/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/haolinnie/Self-Service-Database-Server/?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/cf924c7e3dd6dc57e4f3/maintainability)](https://codeclimate.com/github/haolinnie/Self-Service-Database-Server/maintainability)

Author: Tiger Nie [nhl0819@gmail.com]

Version: 1.1

This is the API server for a Self-Service Database UI for Northwestern Memorial Hospital's Ophthalmology department. The app is written in Python 3.7 with MS SQL as the database layer.

A sample is deployed at https://tigernie.com/ssd_api

## API Documentation

Please read the API documentation to understand the structure of the endpoints. A graphical debugger is available for quick experimentation with the API.

[API documentation.](docs/APIDocumentation.md)

[API debugger](https://tigernie.com/ssd_api)

## Getting Started

Prerequisites

- Python 3.6+
- Docker
- MS SQL Server (Docker image works, script to generate a sample database is provided)

Setting up for

- [Development](#development)
- [Production](#production)

### Development

Download the source code

```bash
git clone https://github.com/haolinnie/Self-Service-Database-Server.git
cd Self-Service-Database-Server
```

#### Create a sample MS SQL database in docker

This pulls a MS SQL Server Ubuntu image from docker, starts a container and dumps sample data into the MS SQL Server.

```bash
make start_dev_db
```

OR

```bash
# Run the MS SQL docker image
docker run --rm -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=yourStrong(!)Password' \
   -p 1433:1433 --name sql1 \
   -d mcr.microsoft.com/mssql/server:2019-GA-ubuntu-16.04

# Copy sample data into the image
docker cp data/create_sample_database_mssql.sql sql1:/tmp

# Initialise sample data in the database
docker exec -it sql1 /opt/mssql-tools/bin/sqlcmd \
   -S localhost -U SA -P "yourStrong(!)Password" \
   -i '/tmp/create_sample_database_mssql.sql'
```

Alternatively, use your existing database server. If so, you must modify the `mssql_url` field in `credentials.config`. The format is

`mssql_url = <SQL dialect>+<SQL driver>://<username>:<password>@<url>:<port>/<database name>`

Only modify username, password, url, port and database name

#### Create a virtual environment and install python dependencies

```bash
make setup
```

OR

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run tests

```bash
make test
```

OR

```bash
source venv/bin/activate
coverage run -m pytest -v
coverage report
coverage html
```


### Production

Download the source code

```bash
git clone https://github.com/haolinnie/Self-Service-Database-Server.git
cd Self-Service-Database-Server
```

Modify the `mssql_url` field in `credentials.config` to plug in your database. Only modify username, password, url, port and database name

`mssql_url = <SQL dialect>+<SQL driver>://<username>:<password>@<url>:<port>/<database name>`

Build the docker image

```bash
make build_api_docker
```

OR

```bash
docker build -t ssd_server:latest .
```

Run the docker image in a container

```bash
make run_api_docker
```

OR

```bash
docker run -d --rm -p 5100:5100 --name ssd_container ssd_server
```

The app runs on port 5100 by default. To change the port, modify both the `Dockerfile` and the `docker run` port number.
