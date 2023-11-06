# FROM php:8.0.2-fpm
# para ambiente de produção usar esta configuração em vez de 
# montagem de volume
# FROM php:8.0.12-fpm-alpine3.13
# FROM php:8.0.12-fpm
FROM php:7.4.25-fpm

RUN apt-get update && apt-get install -y \
    libpq-dev
RUN docker-php-ext-install pdo pdo_pgsql pgsql
# com alpine apt-get não existe
# RUN apt-get update && apt-get install -y \
#     git \
#     curl \
#     zip \
#     vim \
#     unzip
# COPY ./php.ini-production /usr/local/etc/php/php.ini
COPY ./php.ini-development /usr/local/etc/php/php.ini

# WORKDIR /var/www