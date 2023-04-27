#!/bin/bash

python manage.py collectstatic && python manage.py migrate && gunicorn task_manager.wsgi --bind 0.0.0.0:8000
