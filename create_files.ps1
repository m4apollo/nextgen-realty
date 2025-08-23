# create_files.ps1
# Run in PowerShell (Admin Mode)

# Define project root
$projectRoot = "C:\Users\ai realtor ops\Documents\nextgen_realty"

# Define files to create
$filesToCreate = @{
    "mobile/LeadList.tsx" = "React Native component for lead list view"
    "mobile/LeadDetail.tsx" = "React Native component for lead detail view"
    "mobile/ChatSupport.tsx" = "React Native component for in-app chat support"
    "tests/test_mobile_components.js" = "Unit tests for mobile app components"
    "frontend/src/components/KPIDashboard.tsx" = "Next.js component for KPI dashboards"
    "tests/test_analytics.py" = "Unit tests for Analytics agent"
    "tests/test_master_reviewer.py" = "Unit tests for MasterQualityReviewer"
    "n8n_workflows/security_monitoring.json" = "n8n workflow for security monitoring"
}

# Create directories and files
foreach ($file in $filesToCreate.Keys) {
    $fullPath = Join-Path $projectRoot $file
    $directory = Split-Path $fullPath -Parent
    if (-not (Test-Path $directory)) {
        New-Item -ItemType Directory -Path $directory -Force
        Write-Host "Created directory: $directory"
    }
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType File -Path $fullPath -Force
        Write-Host "Created file: $fullPath"
    }
}

Write-Host "File scaffolding complete. Run generate_code.ps1 next."