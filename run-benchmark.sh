#!/bin/bash

# Output folder
output=./results

# Read tests from tests.conf file
tests=$(cat tests.conf)

# Read domains from frameworks.conf file and append .bench to each
domains=$(sed 's/$/.bench/' frameworks.conf | tr '\n' ' ')

# Read commands from commands.conf file, skipping empty lines and comments
commands=$(sed '/^$/d; /^#/d' commands.conf)

# Main loop
for test in $tests; do
    for domain in $domains; do
        while IFS= read -r line; do
            # Extract the command and options
            cmd=$(echo $line | cut -d"=" -f1)
            options=$(echo $line | cut -d"=" -f2-)

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
                    echo "Unknown command: $cmd"
                    continue
                    ;;
            esac

            # First line stores the command line options/args
            echo $options > "$output/$domain.$test.$cmd.log"

            # Execute the docker command
            docker run --rm --network="host" -t $image $options http://$domain:8080/benchmarking/$test | tee -a "$output/$domain.$test.$cmd.log"

            # Cooldown
            echo "Please wait, cooling down for 5 secs..."
            sleep 5
        done <<< "$commands"
    done
done

docker run --rm -v ./www:/www -v ./results:/results bench/python3 /usr/src/app/plot.py
