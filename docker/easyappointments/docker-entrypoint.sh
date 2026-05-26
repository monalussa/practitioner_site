#!/bin/bash
set -e

# Generate config.php from environment variables at container startup.
# This keeps secrets out of source control while using EA's required class-constant format.
cat > /var/www/html/config.php << PHP
<?php
class Config
{
    const BASE_URL    = '${BASE_URL}';
    const LANGUAGE    = 'english';
    const DEBUG_MODE  = ${EA_DEBUG:-false};

    const DB_HOST     = '${DB_HOST}';
    const DB_NAME     = '${DB_NAME}';
    const DB_USERNAME = '${DB_USERNAME}';
    const DB_PASSWORD = '${DB_PASSWORD}';

    const GOOGLE_SYNC_FEATURE  = false;
    const GOOGLE_CLIENT_ID     = '';
    const GOOGLE_CLIENT_SECRET = '';
}
PHP

echo "config.php generated from environment."

# Ensure Apache (www-data) can write sessions, logs, cache, and uploads.
chown -R www-data:www-data /var/www/html/storage

exec apache2-foreground
