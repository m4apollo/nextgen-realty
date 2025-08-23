#!/bin/bash

# Install system dependencies
sudo apt update
sudo apt install -y python3-pip docker.io docker-compose npm

# Install Python dependencies
pip install fastapi sqlmodel stripe langchain-core python-dotenv celery redis uvicorn requests beautifulsoup4 sendgrid

# Setup frontend
cd frontend
npm install
cd ..

# Initialize environment
echo "STRIPE_SECRET_KEY=your_test_key" > .env
echo "ZILLOW_API_KEY=your_zillow_key" >> .env
echo "SENDGRID_API_KEY=your_sendgrid_key" >> .env
echo "COMPANY_NAME=NextGen Realty" >> .env

# Start services
docker-compose up -d

# Initialize database
docker exec nextgen_realty-backend-1 python -c "from db import Base, engine; Base.metadata.create_all(engine)"

# Download AI models
docker exec nextgen_realty-ollama-1 ollama pull llama3
docker exec nextgen_realty-ollama-1 ollama pull mistral
docker exec nextgen_realty-ollama-1 ollama pull codellama

echo "Setup complete! Access the API at http://localhost:8000"