## PHP Frameworks Benchmark

This project allows you to compare the performance of popular PHP frameworks like Laravel, Symfony, CodeIgniter, and others, in a standardized and reproducible environment using Docker containers. You can measure key metrics like Requests Per Second (RPS) and latency for each framework, running the same PHP code base.

## Prerequisites:

- Docker installed and running (https://docs.docker.com/desktop/)
- Git installed and accessible (https://git-scm.com/downloads)

## Supported Platforms:

- Windows (WSL 2 backend)
- macOS
- Linux

## Features:

- Benchmark multiple PHP frameworks with the same code base.
- Measure RPS and latency for each framework.
- Easy to use Docker containers for consistent environment.
- Customizable benchmark configuration.
- Supports running on various platforms.

## Getting Started:

### 1.  Clone the repository:

```bash
git clone https://github.com/bgeneto/php-frameworks-bench
```

### 2. Build the Docker images:

```bash
cd php-frameworks-bench
bash ./build.sh
```

### 3. Check the installation

To check if everything installed correctly and is working as expected, you may need to edit your hosts file (``/etc/hosts` or `C:\Windows\System32\drivers\etc`) and add a line like this:

```
127.0.0.1      laravel.bench codeigniter.bench codeigniter3.bench symfony.bench plainphp.bench
```

(or use a valid IP) Then open your preferred browser and navigate to: 

```
http://codeigniter.bench:8080/benchmarking/info
http://codeigniter3.bench:8080/benchmarking/info
http://laravel.bench:8080/benchmarking/info
http://symfony.bench:8080/benchmarking/info
http://plainphp.bench:8080/benchmarking/info
```

If everything went fine, you should see a standard `phpinfo()` page for each address above:

![image](https://github.com/bgeneto/php-frameworks-bench/assets/473074/82b1fb4d-c1c6-46fb-ab46-ea919be10632)

### 4. Run the benchmark:

Now we are ready to run the benchmarks:

```
bash ./run-benchmark.sh
```


### 5. View the results:

The benchmark report (logs and html files) will be generated in the `results` directory. Some examples of the outputted report/graphics:

![image](https://github.com/bgeneto/php-frameworks-bench/assets/473074/8b4e0db8-3d1f-48cc-b54a-c4e372fd6bdf)

![image](https://github.com/bgeneto/php-frameworks-bench/assets/473074/8e16e038-92aa-4db5-80d6-0d27d5a69fbc)

![image](https://github.com/bgeneto/php-frameworks-bench/assets/473074/0c542ae4-bde6-4cb3-99f1-886c342e3bc0)

## Customization:

You can customize the benchmark by modifying the following files:

- `frameworks.conf`: Define all the (installed) frameworks you would like to be benchmarked. If you are not interested in a framework, you can comment this file like this: 

  ```
  #plainphp
  #codeigniter3
  codeigniter
  symfony
  laravel
  ```

- `tests.conf`: Configure which benchmark test to run (available tests: `info hello api`).

- `benchmarks.conf`: Selects your desired benchmark tool, along with their command line options. You can also comment a benchmark tool you would not like to run (the only tool that will always run is the k6). The example below will run only the `wrk` (and `k6`) benchmarks:

  ```
  # run h2load RPS test
  #h2load=--h1 --warm-up-time 5 -D 10 -c 100 -t 1 -T 5 -m 10
  # run wkr latency and rps test
  wrk=-c 100 -t 1 --timeout 5 -d 10 --latency
  # run wrk2 latency test with constant RPS (requires at least 30s to be accurate!)
  #wrk2=-R 500 -L -d 30s -t 10 -c 100
  ```

  

Other important settings are available in the `conf` folder. For example, if you would like to turn off OPcache, comment the respective line in the file `conf/php/conf.d/docker-php-extensions.ini` : 

```ini
extension=zip
extension=gd
extension=gettext
extension=intl
extension=bcmath
extension=mysqli
extension=pdo_mysql
extension=redis.so
#zend_extension=opcache
```

## Tips/Troubleshooting:

- If you are getting the following errors in `h2load` or `wrk` (or with any other benchmark tool): 

  ```
  getaddrinfo() failed: Name does not resolve
  unable to resolve plainphp.bench:8080 Name does not resolve
  ```

  Then you need to add the line below to your `/etc/hosts` (or `C:\Windows\System32\drivers\etc`):

  ```
  127.0.0.1      laravel.bench codeigniter.bench codeigniter3.bench symfony.bench plainphp.bench
  ```

  And `./run-benchmark.sh` again. 

  > The **./run-benchmark.sh** command may take around **30 minutes** to complete all tests, depending on the processing power of your server! You can decrease this time substantially by removing some tests in the tests.conf file or by removing some frameworks from frameworks.conf. You can also disable some benchmarking tools bt commenting the file benchmarks.conf. 

- It’s a good idea to check whether all docker containers are running and restart then if not:

  ```bash
  docker ps
  docker compose down && docker compose up -d
  ```

  You can also check if all containers are responding as expected with `curl` command:

  ```bash
  curl -v http://laravel.bench:8080/benchmarking/hello
  ```

  The output should be something like this (for all frameworks, not only Laravel, just change the URL)

  ```html
  <!doctype html>
  <html lang="en">
  
  <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Hello</title>
  </head>
  
  <body>
      Hello, World!!!
  </body>
  
  </html>
  ```

  Check also other end points: 

  ```bash
  curl -v http://symfony.bench:8080/benchmarking/api
  ```

  If the api endpoint above fails, check whether the file `films.sql` were imported successfully to our database (Mariadb) container, this is done in the last line from our `./build.sh file`:

  ```bash
  docker exec -i mariadb_bench mysql -ubench -pbench bench < ./src/db/films.sql
  ```

- You can change k6 settings using the template file available in `k6/script.template.js` 

- php-fpm settings are exposed in `conf/php-fpm.d/www.conf` if you want to change my defaults.


## License:

This project is licensed under the GNU GPLv3 License.


## Contributing:

We welcome contributions! Please see the CONTRIBUTING.md file for guidelines on how to contribute.


## Additional Notes:

- This project is a work in progress and may be subject to changes.
- We encourage you to contribute your own benchmarks and test cases.
- Please provide feedback and suggestions through pull requests or issues.



**I hope this helps! Please let me know if you have any questions.**



> **Disclaimer:** Benchmark results may vary depending on your hardware, software, and configuration. This project is intended for comparative analysis and not for absolute performance evaluation.



**Additional Resources:**

- PHP frameworks websites:

  - Laravel: https://laravel.com/
  - Symfony: https://symfony.com/
  - CodeIgniter: https://codeigniter.com/
- Docker documentation: https://docs.docker.com/



**Happy benchmarking!**

