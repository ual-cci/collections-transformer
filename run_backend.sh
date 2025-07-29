#!/bin/bash

cd server/
gunicorn -b 0.0.0.0:8080 -k gevent --workers=12 'app:app(model="openai")' --timeout 600 --preload
