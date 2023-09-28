
#!/bin/bash
set -ex

POSTGRES="psql -U postgres"

# Create the user here. 
# If you puth this value in the docker-compose.yml file, postgres will:
# 1. Create the user losDepende
# 2. Create the database citas. (we do not need this database).
POSTGRES_USER="losDepende"

$POSTGRES <<EOSQL
CREATE USER "${POSTGRES_USER}" WITH SUPERUSER;
CREATE DATABASE "apis-citas" OWNER "${POSTGRES_USER}";
EOSQL
