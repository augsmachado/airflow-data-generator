#!/bin/bash
# Check if the database already exists
if docker compose exec postgres1 psql -U usr1 -d db1 -lqt | cut -d \| -f 1 | grep -qw metabase; then
    echo "Database 'metabase' already exists. Skipping creation."
else
    echo "Creating database 'metabase'..."
    docker compose exec -T postgres1 psql -U usr1 -d db1 -c "CREATE DATABASE metabase;"
fi

# Check if the user already exists
if docker compose exec postgres1 psql -U usr1 -d db1 -c "\du" | grep -q metabase_user; then
    echo "User 'metabase_user' already exists. Skipping creation."
else
    echo "Creating user 'metabase_user'..."
    docker compose exec -T postgres1 psql -U usr1 -d db1 -c "CREATE USER metabase_user WITH PASSWORD 'metabase_password';"
fi

# Grant privileges to the user on the database
echo "Granting privileges to user 'metabase_user' on database 'metabase'..."
docker compose exec -T postgres1 psql -U usr1 -d db1 -c "GRANT ALL PRIVILEGES ON DATABASE metabase TO metabase_user;"

echo "Metabase database setup completed."

