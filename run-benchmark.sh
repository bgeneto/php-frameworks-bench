#!/bin/bash

# Date: 02/17/2024
# Author: Bernhard Enders (bgeneto @ gmail . com)
# This script runs and log all benchmark tests (h2load, wrk, wrk2, k6...)
# so they can be parsed (in python) afterwards.
# Modified: 02/19/2024

# Usage: $ ./run-benchmark.sh

# Output folder
output=./results

# Read benchmarks (end points) from benchmarks.conf file
benchmarks=$(cat benchmarks.conf)

# Read domains from frameworks.conf file and append .bench to each
domains=$(sed '/^#/d' frameworks.conf | sed 's/$/.bench/' | tr '\n' ' ')

# Read commands from benchmarks.conf file, skipping empty lines and comments
commands=$(sed '/^$/d; /^#/d' tests.conf)

# configure the k6 script.js
function replace_uri_in_js() {
  # Error handling: Check for required arguments
  if [[ $# -lt 2 ]]; then
    echo "Usage: replace_uri_in_js <javascript_file> <uri>"
    return 1
  fi

  js_file="$1"
  uri="$2"

  # Perform the replacement (ensure proper quoting)
  sed "s|{{ URI }}|$uri|g" "$js_file" > ./k6/script.js
}

# Main loop
for test in $benchmarks; do
    for domain in $domains; do
        while IFS= read -r line; do
            # Extract the command and options
            cmd=$(echo $line | cut -d"=" -f1)
            cmd_options=$(echo $line | cut -d"=" -f2-)

            # Common docker options/args
            docker_options="--rm --network=host -u $UID"

            # The endpoint/url for the test
            url=http://$domain:8080/benchmarking/$test

            # Determine which docker image to use based on the command
            case "$cmd" in
                h2load)
                    image="openquantumsafe/h2load h2load"
                    ;;
                wrk)
                    image="williamyeh/wrk"
                    ;;
                wrk2)
                    image="cylab/wrk2"
                    ;;
                *)
                    continue
                    ;;
            esac

            # First line stores the command line options/args
            echo $cmd_options > "$output/$domain.$test.$cmd.log"

            # Display test info
            echo ""
            echo "..:: Running $cmd tests at http://$domain:8080/benchmarking/$test ::.."
            echo ""

            # Execute the docker command
            docker run $docker_options -t $image $cmd_options $url | tee -a "$output/$domain.$test.$cmd.log" || true

            # Cooldown
            echo "Please wait, cooling down for 5 secs..."
            sleep 5
        done <<< "$commands"

        # run k6 test (always run k6 test, even if no test is selected)
        cmd="k6"
        image="grafana/k6"
        docker_options+=" -i -v $PWD/k6:/app -v $PWD/results:/results -w /app"
        replace_uri_in_js ./k6/script.template.js http://$domain:8080/benchmarking/$test
        #docker run $docker_options -t $image $cmd_options | tee -a "$output/$domain.$test.$cmd.log"
        echo ""
        echo "..:: Running k6 tests at http://$domain:8080/benchmarking/$test ::.."
        echo ""
        docker run $docker_options $image run --summary-export /results/$domain.$test.$cmd.log - <k6/script.js || true
        sleep 5
    done
done

# plot the results to html file
docker run -u $UID --rm -v ./:/usr/src/app bench/python3 /usr/src/app/plot.py
