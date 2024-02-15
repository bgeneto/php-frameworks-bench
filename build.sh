#!/usr/bin/bash

# build the php-fpm image with all required extensions
docker compose build --parallel

# start all containers
docker compose up -d

# save current user id
userid=$(id -u)
userid=${userid%% *}

# enter php docker container to install all required frameworks via composer
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project codeigniter4/appstarter codeigniter
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project pocketarc/codeigniter codeigniter3
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project symfony/skeleton:"7.0.*" symfony
docker exec -it -u $userid php_fpm_bench bash -c 'cd symfony; composer --no-cache require symfony/twig-bundle'
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project laravel/laravel:"11.x-dev" laravel

# copy our controllers, views, and routes
cp -rf ./src/www/html/* ./www/html/

# some frameworks requires write access to certain folders
# since we can't chown without sudo, the only solution is to give everybody write permission.
chmod -R o+w ./www/html/codeigniter/writable
chmod -R o+w ./www/html/codeigniter3/application/logs
chmod -R o+w ./www/html/codeigniter3/application/cache
chmod -R o+w ./www/html/symfony/var
chmod -R o+w ./www/html/laravel/storage

# restart all containers (just in case)
docker compose down && docker compose up -d

# import database data
docker exec -i mariadb_bench mysql -uroot -p'your-very-long-passwd' bench < /tmp/films.sql