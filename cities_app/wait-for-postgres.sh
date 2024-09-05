#!/bin/sh

until nc -z -v -w30 db 5432
do
  echo "Waiting for database connection..."
  sleep 1
done

exec "$@"
