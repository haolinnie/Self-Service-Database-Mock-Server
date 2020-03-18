#!/bin/bash
export FLASK_ENV=production
./venv/bin/gunicorn -w 2 --bind=0.0.0.0:5100 \
    "api:create_app()"
