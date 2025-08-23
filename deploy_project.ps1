# deploy_project.ps1
# Run in PowerShell (Admin Mode)

# Define project root
$projectRoot = "C:\Users\ai realtor ops\Documents\nextgen_realty"

# Configure .env files
$backendEnv = Join-Path $projectRoot "backend/.env"
$frontendEnv = Join-Path $projectRoot "frontend/.env"
$envContent = @"
DATABASE_URL=sqlite:///$projectRoot/backend/db.sqlite
STRIPE_API_KEY=sk_test_xxx
OLLAMA_API_URL=http://localhost:11434
"@
Set-Content -Path $backendEnv -Value $envContent
Set-Content -Path $frontendEnv -Value $envContent

# Run setup script
$setupScript = Join-Path $projectRoot "scripts/setup.sh"
if (Test-Path $setupScript) {
    Write-Host "Running setup script..."
    wsl bash $setupScript
} else {
    Write-Host "setup.sh not found. Skipping..."
}

# Start Docker Compose
$dockerCompose = Join-Path $projectRoot "docker/docker-compose.yml"
if (Test-Path $dockerCompose) {
    Write-Host "Starting Docker Compose..."
    docker-compose -f $dockerCompose up -d
} else {
    Write-Host "Creating docker-compose.yml..."
    $dockerComposeContent = @"
version: '3.8'
services:
  backend:
    build: $projectRoot/backend
    ports:
      - '8000:8000'
    volumes:
      - $projectRoot/backend:/app
    environment:
      - DATABASE_URL=sqlite:////app/db.sqlite
      - STRIPE_API_KEY=sk_test_xxx
      - OLLAMA_API_URL=http://ollama:11434
  frontend:
    build: $projectRoot/frontend
    ports:
      - '3000:3000'
    volumes:
      - $projectRoot/frontend:/app
  ollama:
    image: ollama/ollama
    ports:
      - '11434:11434'
  prometheus:
    image: prom/prometheus
    ports:
      - '9090:9090'
  grafana:
    image: grafana/grafana
    ports:
      - '3001:3000'
"@
    $dockerComposeDir = Split-Path $dockerCompose -Parent
    New-Item -ItemType Directory -Path $dockerComposeDir -Force
    Set-Content -Path $dockerCompose -Value $dockerComposeContent
    docker-compose -f $dockerCompose up -d
}

Write-Host "Deployment complete. Access frontend at http://localhost:3000, backend at http://localhost:8000."