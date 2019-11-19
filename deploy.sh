#!/usr/bin/env bash

if [[ -z "$DB_PASSWORD" ]]; then
    echo "Specify DB_PASSWORD in environment" 1>&2
    exit 1
fi

if [[ -z "$APP_SECRET_KEY" ]]; then
    echo "Specify APP_SECRET_KEY in environment" 1>&2
    exit 1
fi

if [[ -z "$PORT" ]]; then
    export PORT=80
fi

docker-compose -f ./docker/compose.yaml --no-ansi up --build
