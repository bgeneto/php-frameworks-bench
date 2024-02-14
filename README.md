## PHP Frameworks Benchmark

This project allows you to compare the performance of popular PHP frameworks like Laravel, Symfony, CodeIgniter, and others, in a standardized and reproducible environment using Docker containers. You can measure key metrics like Requests Per Second (RPS) and latency for each framework, running the same PHP code base.

## Prerequisites:

- Docker installed and running (https://docs.docker.com/desktop/)
- Git installed and accessible (https://git-scm.com/downloads)

## Supported Platforms:

- Windows (WSL2)
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

```bat
127.0.0.1      laravel.bench codeigniter.bench codeigniter3.bench symfony.bench plainphp.bench
```

Then open your preferred browser and navigate to: 

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

- `frameworks.conf`: Define all the frameworks you would like to be benchmarked.
- `tests.conf`: Configure which benchmark test to run.
- `commands.conf`: Your preferred command line options for each benchmark tool used.


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

