#!/usr/bin/sh

# build the php-fpm image with all required extensions
docker compose build --parallel

# start all containers
docker compose up -d

# enter php docker container to install all required frameworks via composer
docker exec -it php_fpm_bench composer create-project codeigniter4/appstarter codeigniter
docker exec -it php_fpm_bench composer create-project symfony/skeleton:"7.0.*" symfony
docker exec -it php_fpm_bench bash -c 'cd symfony; composer require symfony/twig-bundle'
docker exec -it php_fpm_bench composer create-project laravel/laravel:"11.x-dev" laravel
docker exec -it php_fpm_bench composer create-project pocketarc/codeigniter codeigniter3

# save current user id
userid=$(id -u)
userid=${userid%% *}

# set the right permissions to www-data
echo -e "We need 'sudo' to copy files and set the proper ownership:\n"

sudo cp -r ./src/* ./www/html/
sudo chown -R 33:$userid ./www

# restart all containers (just in case)
docker compose down && docker compose up -d
