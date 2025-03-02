#!/bin/bash

# Initialize the database if the --init-db flag is passed
if [ "$1" = "--init-db" ]; then
    echo "Initializing database..."
    python -m app.db.init_db
    exit 0
fi

# Run the command passed to docker
exec "$@"