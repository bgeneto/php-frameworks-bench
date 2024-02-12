# php-frameworks-bench
Docker containers to benchmark several php frameworks

## Install Instructions

```bash
git clone https://github.com/bgeneto/php-frameworks-bench.git
cd php-frameworks-bench
docker compose build --parallel
docker compose up -d
# enter php docker container to install all required frameworks via composer
docker exec -it php-fpm bash
sh ./composer-install.sh
# extract our controllers, views, routes...
unzip -o html.zip
# exit docker container
exit
```
 
