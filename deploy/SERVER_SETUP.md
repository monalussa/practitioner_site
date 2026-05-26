# Setup Guide

## Local Development

### Prerequisites
- Python 3.12+
- Docker + docker-compose-v2: `sudo apt install -y docker.io docker-compose-v2`
- Add yourself to the docker group: `sudo usermod -aG docker $USER && newgrp docker`

### Django / Wagtail (main site)
```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env        # fill in SECRET_KEY and DATABASE_URL at minimum
DJANGO_SETTINGS_MODULE=config.settings.dev .venv/bin/python manage.py migrate
DJANGO_SETTINGS_MODULE=config.settings.dev .venv/bin/python manage.py seed_content
DJANGO_SETTINGS_MODULE=config.settings.dev .venv/bin/python manage.py createsuperuser
DJANGO_SETTINGS_MODULE=config.settings.dev .venv/bin/python manage.py runserver
```
Site available at http://localhost:8000 · Admin at http://localhost:8000/admin/

### Easy!Appointments (booking)
```bash
cp .env.booking.example .env.booking   # default values work for local dev
docker compose --env-file .env.booking build
docker compose --env-file .env.booking up -d
```
1. Open http://localhost:9090 — complete the installation wizard (one-time)
2. In Wagtail admin → Pages → "Book a Session": set `booking_url` to `http://localhost:9090`, check `embed_booking`, publish

### Stopping the booking stack
```bash
docker compose --env-file .env.booking down
```

---

# VPS Setup Guide (Namecheap Ubuntu 22.04)

## 1. Initial server setup

```bash
sudo apt update && sudo apt upgrade -y

# Django/Wagtail dependencies
sudo apt install -y nginx python3.12 python3.12-venv python3-pip \
    postgresql postgresql-contrib certbot python3-certbot-nginx

# Docker + Compose (for Easy!Appointments)
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER   # allows deploy user to run docker without sudo
# Log out and back in (or run: newgrp docker) for group change to take effect
```

## 2. Create deploy user

```bash
sudo adduser deploy
sudo usermod -aG www-data deploy
```

## 3. Upload the app

```bash
# From your local machine:
rsync -av --exclude='.venv' --exclude='db.sqlite3' --exclude='staticfiles' \
    /path/to/practitioner-site/ deploy@YOUR_VPS_IP:/home/deploy/practitioner-site/
```

## 4. Set up Python environment

```bash
cd /home/deploy/practitioner-site
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## 5. Configure PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE coaching_db;
CREATE USER coaching_user WITH PASSWORD 'strong-password-here';
GRANT ALL PRIVILEGES ON DATABASE coaching_db TO coaching_user;
\q
```

## 6. Configure .env

Copy `.env.example` to `.env` and fill in all values:
- `SECRET_KEY`: generate with `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`
- `DATABASE_URL`: `postgres://coaching_user:strong-password-here@localhost:5432/coaching_db`
- `ALLOWED_HOSTS`: `yourdomain.com,www.yourdomain.com`
- Email settings (Namecheap mail or Gmail app password)

## 7. Run migrations and collect static

```bash
DJANGO_SETTINGS_MODULE=config.settings.production .venv/bin/python manage.py migrate
DJANGO_SETTINGS_MODULE=config.settings.production .venv/bin/python manage.py collectstatic --no-input
DJANGO_SETTINGS_MODULE=config.settings.production .venv/bin/python manage.py createsuperuser
```

## 8. Set up Gunicorn systemd service

```bash
sudo mkdir -p /var/log/gunicorn
sudo chown deploy:deploy /var/log/gunicorn
sudo cp deploy/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

## 9. Configure Nginx

```bash
sudo cp deploy/nginx-main-site.conf /etc/nginx/sites-available/yourdomain.com
sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

## 10. SSL with Certbot

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
# Auto-renew is set up by certbot. Verify:
sudo systemctl status certbot.timer
```

## 11. Deploy Easy!Appointments via Docker

The app ships with `docker-compose.yml` which runs EA + MySQL as containers.
PHP and MySQL are NOT installed directly on the server — Docker manages them.

The `docker-entrypoint.sh` generates `config.php` from env vars at startup and runs
`chown -R www-data:www-data storage/` so Apache can write session files, logs, cache,
and uploads. This is why no manual PHP session configuration is needed.

```bash
# On the server, inside the project directory:

# Create the production env file (never commit this)
cp .env.booking.example .env.booking.prod
# Edit .env.booking.prod — set real passwords and the production BASE_URL:
#   BASE_URL=https://book.yourdomain.com/
#   DB_PASSWORD=<strong-random-password>
#   MYSQL_PASSWORD=<same-as-DB_PASSWORD>
#   MYSQL_ROOT_PASSWORD=<different-strong-password>
#   EA_DEBUG=false
nano .env.booking.prod

# Start the containers
docker compose --env-file .env.booking.prod up -d
```

```bash
# Add Nginx reverse-proxy config for booking subdomain
sudo cp deploy/nginx-booking-docker.conf /etc/nginx/sites-available/book.yourdomain.com
sudo ln -s /etc/nginx/sites-available/book.yourdomain.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d book.yourdomain.com
```

Visit `https://book.yourdomain.com` to complete the Easy!Appointments setup wizard.

## 12. Update Wagtail booking page

In the Wagtail admin: go to the Booking Page and set the `booking_url` field to `https://book.yourdomain.com`.

## Ongoing deploys

```bash
# Upload new code then run:
bash deploy/deploy.sh
```
