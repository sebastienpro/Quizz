#!/usr/bin/env bash
set -e

python3 ./manage.py migrate
exec gunicorn Quizz.wsgi -w ${WORKERS:=4} -b :8000 --reload