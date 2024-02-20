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
docker exec -it -u $userid php_fpm_bench composer --no-cache create-project laravel/laravel:"11.x-dev" octane
docker exec -it -u $userid php_fpm_bench bash -c 'cd octane; composer --no-cache --no-interaction require laravel/octane'
#docker exec -it -u $userid php_fpm_bench bash -c 'cd octane; php artisan octane:install --server=swoole --no-interaction'
docker exec -it -u $userid php_fpm_bench bash -c 'cd octane; composer --no-cache --no-interaction require spiral/roadrunner-cli spiral/roadrunner-http'
docker exec -it -u $userid php_fpm_bench bash -c 'cd octane; php artisan octane:install --server=roadrunner --no-interaction'

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

# restart all containers (after changing the command)
docker compose down && docker compose up -d

# for containers to be ready
sleep 5

# import database data
max_retries=5
retry_count=0
wait_time=1  # Seconds to wait between retries

while true; do
  docker exec -i mariadb_bench mysql -ubench -pbench bench < ./src/db/films.sql

  if [ $? -eq 0 ]; then
    echo "Database data imported successfully!"
    break
  else
    retry_count=$((retry_count + 1))

    if [ $retry_count -ge $max_retries ]; then
      echo "Command failed after $max_retries retries. Exiting."
      exit 1
    fi
    sleep $wait_time
  fi
done
