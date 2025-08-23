#!/bin/bash

# Build and deploy the application
docker-compose down
docker-compose build --no-cache
docker-compose up -d --force-recreate

# Run database migrations
docker exec nextgen_realty-backend-1 python -c "from db import Base, engine; Base.metadata.create_all(engine)"

echo "Deployment complete! Services are running."