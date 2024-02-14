#!/usr/bin/bash

IFS=' '

tests="hello info"
domains="plainphp.bench codeigniter3.bench codeigniter.bench symfony.bench laravel.bench"

for test in $tests; do
    for domain in $domains; do
        # run h2load bench and log to file
        docker run --rm --network="host" -t openquantumsafe/h2load h2load --h1 --warm-up-time 5 -D 10 -c 100 -t 1 -T 5 -m 10 -H "Accept-Encoding: gzip" "http://$domain:8080/benchmarking/$test" | tee "./logs/$domain.$test.h2load.log"
        # cooldown
        sleep 5
    done
done

docker run --rm -v ./logs:/logs bench/python3 /usr/src/app/plot.py
