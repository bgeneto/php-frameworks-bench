FROM php:fpm-bookworm

COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer

ENV CFLAGS "-O3 -march=native"
ENV CPPFLAGS "$CFLAGS"
ENV PHP_CFLAGS "-fstack-protector-strong -fpic -fpie -O3 -march=native -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
ENV PHP_CPPFLAGS "$PHP_CFLAGS"

RUN apt update && apt install -y \
        libfreetype6-dev nano unzip \
        libjpeg62-turbo-dev zip libzip-dev \
        libpng-dev iproute2 iputils-ping zlib1g-dev libicu-dev \
        libcurl4-openssl-dev libonig-dev
RUN sh -c 'pecl list | grep -q redis || (pecl install redis && docker-php-ext-enable redis)'
RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-configure zip
RUN docker-php-ext-install -j$(nproc) gd mysqli intl zip pdo gettext pdo_mysql bcmath
RUN docker-php-ext-enable redis
RUN rm -rf /var/lib/apt/lists/*

