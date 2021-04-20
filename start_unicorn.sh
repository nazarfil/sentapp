#!/bin/sh
gunicorn --workers=1 wsgi:app --threads 2 -b 0.0.0.0:6000
gunicorn --worker-class=gevent --worker-connections=1000 --workers=3 --threads=2 wsgi:client_app --threads 2 -b 0.0.0.0:5000