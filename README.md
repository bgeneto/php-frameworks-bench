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
# give permissions to www-data user
chown -R www-data:1000 /var/www
chmod g+w /var/www
# exit docker container
exit
# restart all containers (just in case)
docker compose down
docker compose up -d
```
 
## Check installation 

Edit your hosts file (/etc/hosts or C:\Windows\System32\drivers\etc) and add this line:

```
127.0.0.1      laravel.localhost codeigniter.localhost symfony.localhost plainphp.localhost
```

Now open your preferred browser and navigate to: 

```
http://codeigniter.localhost:8080/benchmarking/info
http://laravel.localhost:8080/benchmarking/info
http://symfony.localhost:8080/benchmarking/info
http://plainphp.localhost:8080/benchmarking/info
```

If everything went fine, you should see a standard `phpinfo()` page like this:

![image](https://github.com/bgeneto/php-frameworks-bench/assets/473074/82b1fb4d-c1c6-46fb-ab46-ea919be10632)

