#!/bin/sh
python manage.py migrate --noinput  && \
python manage.py collectstatic --noinput  && \
#python init_data_database.py && \
uwsgi --ini /code/docker/dev/django/uwsgi.ini