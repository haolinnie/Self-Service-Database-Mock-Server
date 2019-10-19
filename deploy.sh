#!/bin/sh
gunicorn -w 2 --bind=127.0.0.1:5100 "ssd_api:create_app"
