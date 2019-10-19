#!/bin/bash
source ./flask/bin/activate
gunicorn -w 2 --bind=127.0.0.1:5100 app:app
