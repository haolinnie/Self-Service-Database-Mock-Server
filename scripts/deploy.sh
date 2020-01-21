#!/bin/bash
./venv/bin/gunicorn -w 2 --bind=0.0.0.0:5100 \
    "api:create_app()"
