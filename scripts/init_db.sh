#!/bin/bash

set -x
set -eo pipefail

# Check if psql is installed
if ! [ -x "$(command -v psql)" ]; then
    echo "Error : $(psql) is not installed"
    exit 1
fi

# check if a custom user has been set, otherwise default to "postgres"
DB_USER=${POSTGRES_USER:=postgres}
# check if a custom password has been set, otherwise default to "password"
DB_PASS=${POSTGRES_PASSWORD:=password}
# check if a custom database name has been set, otherwise default to "newsletter"
DB_NAME=${POSTGRES_DB:=pdf_intellect}
# check if a custom port host has been set, otherwise default to "5432"
DB_PORT=${POSTGRES_PORT:=5432}

#  Allow to skip Docker if a dockerized database is already available

# Launch postgres using Docker
if [[ -z "${SKIP_DOCKER}" ]]; then
    docker run \
        -e POSTGRES_USER=${DB_USER} \
        -e POSTGRES_PASSWORD=${DB_PASS} \
        -e POSTGRES_DB=${DB_NAME} \
        -p ${DB_PORT}:5432 \
        -d postgres \
        postgres -N 1000
fi
# Increased max number of connection for testing purposes
# Keep pinging postgres unti it is ready to accept commands
export PGPASSWORD=${DB_PASS}

until psql -h "localhost" -U "${DB_USER}" -p "${DB_PORT}" -d "postgres" -c '\q'; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

echo >&2 "Postgres is up and running on port ${DB_PORT}"

# Drop the database if it exists

psql -h localhost -U postgres -p 5432 -c "DROP DATABASE IF EXISTS ${DB_NAME};"

# Create the database
psql -h localhost -U postgres -p 5432 -c "CREATE DATABASE ${DB_NAME};"

# Create the extension for storing vectors
psql -h localhost -U postgres -p 5432 -d ${DB_NAME} -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Create the table for storing document embeddings
psql -h localhost -U postgres -p 5432 -d ${DB_NAME} -c "DROP TABLE IF EXISTS documents;"

psql -h localhost -U postgres -p 5432 -d ${DB_NAME} -c "CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    metadata JSONB NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL
);"
