#!/bin/bash
export DJANGO_SUPERUSER_PASSWORD="ffw_J771"
export DJANGO_SUPERUSER_USERNAME="admin"
export DJANGO_SUPERUSER_EMAIL="admin@mail.io"
# env
python manage.py createsuperuser --noinput
# python manage.py createsuperuser --username admin --email admin@mail.io