#!/bin/bash
# Run on the VPS as the deploy user after uploading new code.
set -e

APP_DIR=/home/deploy/practitioner-site
VENV=$APP_DIR/.venv

cd $APP_DIR

$VENV/bin/pip install -r requirements.txt --quiet
DJANGO_SETTINGS_MODULE=config.settings.production $VENV/bin/python manage.py migrate --no-input
DJANGO_SETTINGS_MODULE=config.settings.production $VENV/bin/python manage.py collectstatic --no-input

sudo systemctl restart gunicorn
echo "Deploy complete."
