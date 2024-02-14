#!/usr/bin/bash

IFS=' '

tests="hello info"
domains="plainphp.bench codeigniter3.bench codeigniter.bench symfony.bench laravel.bench"

for test in $tests; do
    for domain in $domains; do
        # run h2load bench and log to file
        docker run --rm --network="host" -t openquantumsafe/h2load h2load --h1 --warm-up-time 5 -D 10 -c 100 -t 1 -T 5 -m 10 -H "Accept-Encoding: gzip" "http://$domain:8080/benchmarking/$test" | tee "./results/$domain.$test.h2load.log"
        # run wkr latency and rps test
        docker run --rm --network="host" -t williamyeh/wrk -c 100 -t 1 --timeout 5 -d 10 --latency "http://$domain:8080/benchmarking/$test" | tee "./results/$domain.$test.wrk.log"
        # run wrk2 latency test with constant RPS
        docker run --rm --network="host" -t cylab/wrk2 -c 100 -t 1 --timeout 5 -d 10 -R 1000 --latency "http://$domain:8080/benchmarking/$test" | tee "./results/$domain.$test.wrk2.log"
        # cooldown
        echo "Please wait, cooling down..."
        sleep 5
    done
done

docker run --rm -v ./www:/www -v ./results:/results bench/python3 /usr/src/app/plot.py
