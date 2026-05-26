FROM php:8.2-apache

RUN apt-get update && apt-get install -y \
    libicu-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libzip-dev \
    libonig-dev \
    && docker-php-ext-install mysqli pdo_mysql intl xml curl zip mbstring \
    && a2enmod rewrite \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/lib/php/sessions \
    && chown www-data:www-data /var/lib/php/sessions \
    && chmod 750 /var/lib/php/sessions

RUN echo "session.save_path = /var/lib/php/sessions" > /usr/local/etc/php/conf.d/sessions.ini \
    && echo "session.gc_probability = 1" >> /usr/local/etc/php/conf.d/sessions.ini

COPY apache.conf /etc/apache2/sites-available/000-default.conf
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
