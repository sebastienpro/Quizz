#!/usr/bin/env bash
set -e

python3 ./manage.py migrate
python3 ./manage.py collectstatic --noinput
exec gunicorn Quizz.wsgi -w ${WORKERS:=4} -b :8000 --reload