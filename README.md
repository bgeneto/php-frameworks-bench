# php-frameworks-bench
Docker containers to benchmark several php frameworks

## Install Instructions

```bash
git clone https://github.com/bgeneto/php-frameworks-bench.git
cd php-frameworks-bench
unizp html.zip
docker compose build --parallel
docker compose up -d
docker exec -it php-fpm bash
# install codeigniter 4 framework (inside php-fpm docker container):
cd /var/www/html/codeigniter
composer require codeigniter4/appstarter
# install symfony
cd ../symfony/
composer require symfony/skeleton:"7.0.*"
# install laravel
cd ../laravel/
composer require laravel/laravel:"11.x-dev"
```
 
