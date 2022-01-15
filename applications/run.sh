#!/bin/bash 
gunicorn -b 0.0.0.0:8080 --workers 4 main:app --worker-class uvicorn.workers.UvicornWorker --preload --timeout 120