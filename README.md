## PHP Frameworks Benchmark

This project allows you to compare the performance of popular PHP frameworks like Laravel, Symfony, CodeIgniter, and others, in a standardized and reproducible environment using Docker containers. You can measure key metrics like Requests Per Second (RPS) and latency for each framework, running the same PHP code base.

## Prerequisites:

- Docker installed and running (https://docs.docker.com/desktop/)
- Git installed and accessible (https://git-scm.com/downloads)

## Supported Platforms:

- Windows
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
cd php-frameworks-benchmark
sh ./build.sh
```

### 3. Check the installation

To check if everything installed correctly and is working as expected, you may need to edit your hosts file (``/etc/hosts` or `C:\Windows\System32\drivers\etc`) and add a line like this:

```bat
127.0.0.1      laravel.localhost codeigniter.localhost symfony.localhost plainphp.localhost
```

Then open your preferred browser and navigate to: 

```
http://codeigniter.localhost:8080/benchmarking/info
http://laravel.localhost:8080/benchmarking/info
http://symfony.localhost:8080/benchmarking/info
http://plainphp.localhost:8080/benchmarking/info
```

If everything went fine, you should see a standard `phpinfo()` page for each address above:

![image](https://github.com/bgeneto/php-frameworks-bench/assets/473074/82b1fb4d-c1c6-46fb-ab46-ea919be10632)

### 4. Run the benchmark:

Now we are ready to run the benchmarks:

```
./run-benchmark.sh [options]
```

Available options:

- `--frameworks`: Comma-separated list of frameworks to benchmark (e.g., `laravel,symfony,codeigniter`).
- `--iterations`: Number of iterations for each benchmark (default: 10).
- `--concurrency`: Number of concurrent requests per iteration (default: 10).
- `--help`: Display help message.


### 5. View the results:

The benchmark report will be generated in the `results` directory.

## Customization:

You can customize the benchmark by modifying the following files:

- `benchmarks.php`: Define the PHP code to be benchmarked.
- `configuration.json`: Configure the benchmark settings like iterations, concurrency, and frameworks.


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

