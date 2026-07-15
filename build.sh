#!/usr/bin/env bash
# Render/PaaS build script for the Wagtail showcase site.
# Runs with DJANGO_SETTINGS_MODULE=config.settings.production set in the host env.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input

# seed_content is idempotent (every page is guarded by an .exists() check),
# so it is safe to run on every deploy.
python manage.py seed_content

# Bootstrap the Wagtail admin superuser from env vars, if provided.
# Skips cleanly when the user already exists so redeploys don't fail.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input || true
fi
