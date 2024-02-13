#!/usr/bin/sh

# build the php-fpm image with all required extensions
docker compose build --parallel

# start all containers
docker compose up -d

# enter php docker container to install all required frameworks via composer
docker exec -it php_fpm_fmbench composer create-project codeigniter4/appstarter codeigniter
docker exec -it php_fpm_fmbench composer create-project symfony/skeleton:"7.0.*" symfony
docker exec -it php_fpm_fmbench composer require symfony/twig-bundle
docker exec -it php_fpm_fmbench composer create-project laravel/laravel:"11.x-dev" laravel
docker exec -it php_fpm_fmbench composer create-project pocketarc/codeigniter codeigniter3

# copy our controllers, views, routes to each framework
cp -r ./src/* ./www/html/

# set the right permissions to www-data
echo -e "We need 'sudo' to set the proper ownership in 'www' folder to 'www-data' user:\n"
userid=`echo $UID`
sudo chown -R 33:$userid ./www

# restart all containers (just in case)
docker compose down && docker compose up -d
