# php-frameworks-bench
Docker containers to benchmark several php frameworks

## Instructions

```bash
git clone https://github.com/bgeneto/php-frameworks-bench.git
cd php-frameworks-bench
unizp html.zip
docker compose build --parallel
docker compose up -d
docker exec -it php-fpm bash
# install codeigniter 4 framework
cd codeigniter
composer update
# install symfony
cd ../symfony/
composer update
# install laravel
cd ../laravel/
composer update
```
 
