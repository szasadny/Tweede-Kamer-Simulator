#!/bin/bash

# Wait for the database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Initialize the database if the --init-db flag is passed
if [ "$1" = "--init-db" ]; then
    echo "Initializing database..."
    python -m app.db.init_db
    exit 0
fi

# Run database migrations (if applicable)
# Uncomment and adjust if using Alembic or another migration tool
# alembic upgrade head

# Run the command passed to docker
exec "$@"