# Conscious Parenting Coach — Website

A coaching website with CMS-managed content and an integrated online booking system.

## Tech stack

| Layer | Technology |
|---|---|
| Main site | Django 5 + Wagtail 7 (Python) |
| CMS | Wagtail admin — no code needed to edit content |
| Booking | Easy!Appointments 1.5.x (PHP, runs in Docker) |
| Database (site) | PostgreSQL (production) / SQLite (local dev) |
| Database (booking) | MySQL 8 (inside Docker) |
| Static files | WhiteNoise |
| SEO | wagtail-seo (per-page meta, Schema.org JSON-LD, sitemap) |

## Quick local start

```bash
# 1. Main site
cp .env.example .env          # fill in SECRET_KEY at minimum
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
DJANGO_SETTINGS_MODULE=config.settings.dev .venv/bin/python manage.py migrate
DJANGO_SETTINGS_MODULE=config.settings.dev .venv/bin/python manage.py seed_content
DJANGO_SETTINGS_MODULE=config.settings.dev .venv/bin/python manage.py createsuperuser
DJANGO_SETTINGS_MODULE=config.settings.dev .venv/bin/python manage.py runserver

# 2. Booking system (requires Docker)
cp .env.booking.example .env.booking
docker compose --env-file .env.booking build
docker compose --env-file .env.booking up -d
# Then open http://localhost:9090 and complete the setup wizard (one-time)
```

- Main site: http://localhost:8000
- Wagtail admin: http://localhost:8000/admin/
- Booking admin: http://localhost:9090/index.php/login

## Project structure

```
config/          Django settings (base / dev / production)
pages/           Wagtail page models and management commands
contact/         Contact form app
templates/       All HTML templates
static/css/      main.css — full design system
easyappointments-1.5.2/  Easy!Appointments (PHP)
docker/          Dockerfile + entrypoint for the booking container
deploy/          Server setup guide, Nginx configs, Gunicorn service
seo/             Keyword reference and SEO checklist
```

## Deployment

See [deploy/SERVER_SETUP.md](deploy/SERVER_SETUP.md) for the complete VPS setup guide.

## Environment files

| File | Committed | Purpose |
|---|---|---|
| `.env.example` | Yes | Template for Django settings |
| `.env` | No | Local Django secrets |
| `.env.booking.example` | Yes | Template for booking/Docker settings |
| `.env.booking` | No | Local booking secrets |
| `.env.booking.prod` | No | Production booking secrets |
