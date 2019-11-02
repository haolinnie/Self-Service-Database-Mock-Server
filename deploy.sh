#!/bin/bash
source ./flask/bin/activate
gunicorn -w 2 --bind=0.0.0.0:5100 app:app
