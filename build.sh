#!/usr/bin/bash

# build the php-fpm image with all required extensions
docker compose build --parallel

# start all containers
docker compose up -d

# save current user id
userid=$(id -u)
userid=${userid%% *}

# wait for containers to be ready
sleep 5

# enter php docker container to install all required frameworks via composer
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project codeigniter4/appstarter codeigniter
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project pocketarc/codeigniter codeigniter3
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project symfony/skeleton:"7.0.*" symfony
docker exec -it -u $userid php_fpm_bench bash -c 'cd symfony; composer --no-cache --no-interaction require symfony/twig-bundle'
docker exec -it -u $userid php_fpm_bench bash -c 'cd symfony; composer --no-cache --no-interaction require symfony/orm-pack'
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project laravel/laravel:"11.x-dev" laravel
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project laravel/laravel:"10.x" octane
docker exec -it -u $userid php_fpm_bench bash -c 'cd octane; composer --no-cache --no-interaction require laravel/octane'
docker exec -it -u $userid php_fpm_bench bash -c 'cd octane; php artisan octane:install --server=swoole'

# copy our controllers, views, and routes
cp -rf ./src/www/html/* ./www/html/

# some frameworks requires write access to certain folders
# since we can't chown without sudo, the only solution is to give everybody write permission.
chmod -R o+w ./www/html/codeigniter/writable
chmod -R o+w ./www/html/codeigniter3/application/logs
chmod -R o+w ./www/html/codeigniter3/application/cache
chmod -R o+w ./www/html/symfony/var
chmod -R o+w ./www/html/laravel/storage
chmod -R o+w ./www/html/octane/storage

# remove the comment in #command:
sed -i 's/^\([[:space:]]*\)#command:/\1command:/' "./docker-compose.yml"

# restart all containers (after changing the command)
docker compose down && docker compose up -d

# import database data
sleep 5
docker exec -i mariadb_bench mysql -ubench -pbench bench < ./src/db/films.sql
