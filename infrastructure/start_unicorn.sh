#!/bin/sh
gunicorn wsgi:app -w 1 --threads 2 -b 0.0.0.0:5000