#!/bin/bash

# The database parameters
DBNAME="vector_db"
USER="yasirdev"
PASSWORD=""
HOST="localhost"

# Drop the database if it exists
psql -h $HOST -U $USER -c "DROP DATABASE IF EXISTS $DBNAME;"

# Create the database
psql -h $HOST -U $USER -c "CREATE DATABASE $DBNAME;"

# Create the extension for storing vectors
psql -h $HOST -U $USER -d $DBNAME -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Create the table for storing document embeddings
psql -h $HOST -U $USER -d $DBNAME -c "DROP TABLE IF EXISTS documents;"

psql -h $HOST -U $USER -d $DBNAME -c "
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    metadata JSONB NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL
);
"
