#!/bin/sh
set -e

# first arg is `-f` or `--some-option`
if [ "${1#-}" != "$1" ]; then
	set -- php-fpm "$@"
fi

# Check if the "octane" directory exists
if [ -d "octane" ]; then
    echo "Starting Octane..."
    # Navigate to the octane directory and start Octane in the background
    cd octane && php artisan octane:start --host 0.0.0.0 &
else
    echo "Octane directory not found. Skipping Octane start this time."
fi

# Execute the command specified in CMD or the command line
exec "$@"
