#!/usr/bin/bash

IFS=' '
domains="plainphp.bench codeigniter3.bench codeigniter.bench symfony.bench laravel.bench"
for domain in $domains; do
    # run h2load bench and log to file
    docker run --rm --network="host" -t openquantumsafe/h2load h2load --h1 --warm-up-time 5 -D 10 -c 100 -t 1 -T 5 -m 10 -H "Accept-Encoding: gzip" "http://$domain:8080/benchmarking/info" | tee "./logs/$domain.h2load.log"
    # cooldown
    sleep 5
done


