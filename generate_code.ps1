# generate_code.ps1
# Run in PowerShell (Admin Mode)

# Define project root and Ollama API
$projectRoot = "C:\Users\ai realtor ops\Documents\nextgen_realty"
$ollamaApi = "http://localhost:11434/api/generate"

# Define prompts for DeepSeek
$filePrompts = @{
    "mobile/LeadList.tsx" = "Generate a React Native TypeScript component for a lead list view. Display lead name, email, and status in a FlatList. Include navigation to a LeadDetail screen. Use Expo and tailwind-react-native-classnames. Export the component as default."
    "mobile/LeadDetail.tsx" = "Generate a React Native TypeScript component for a lead detail view. Show lead name, email, status, interaction timeline (array of {date, message}), and property summary (address, price). Use Expo and tailwind-react-native-classnames. Export as default."
    "mobile/ChatSupport.tsx" = "Generate a React Native TypeScript component for in-app chat support. Include a text input and message list, fetching messages from /api/support endpoint. Use Expo and tailwind-react-native-classnames. Export as default."
    "tests/test_mobile_components.js" = "Generate Jest unit tests for React Native components LeadList, LeadDetail, and ChatSupport. Mock navigation and API calls. Test rendering and basic interactions."
    "frontend/src/components/KPIDashboard.tsx" = "Generate a Next.js TypeScript component for a KPI dashboard. Display MRR, CAC, and churn metrics in a grid with Chart.js bar charts. Fetch data from /api/analytics. Use Tailwind CSS. Export as default."
    "tests/test_analytics.py" = "Generate Pytest unit tests for a FastAPI Analytics agent. Test endpoints /api/analytics/mrr, /api/analytics/cac, and /api/analytics/churn. Mock SQLModel database queries."
    "tests/test_master_reviewer.py" = "Generate Pytest unit tests for a FastAPI MasterQualityReviewer agent. Test output monitoring and drift detection logic. Mock AI agent outputs."
    "n8n_workflows/security_monitoring.json" = "Generate an n8n workflow JSON for security monitoring. Include a Schedule Trigger (every 5 minutes), HTTP Request node to query Prometheus (http://prometheus:9090/api/v1/query, query: rate(http_requests_total{status=~'5..'}[5m]) > 0.01), and HTTP Request node to send alerts to Alertmanager (http://alertmanager:9093/api/v1/alerts)."
}

# Function to call Ollama API
function Invoke-Ollama {
    param (
        [string]$prompt,
        [string]$outputFile
    )
    $body = @{
        model = "deepseek-r1:1.5b" # Adjust to your model (e.g., llama3, mistral)
        prompt = $prompt
        stream = $false
    } | ConvertTo-Json
    try {
        $response = Invoke-RestMethod -Uri $ollamaApi -Method Post -Body $body -ContentType "application/json"
        $code = $response.response
        Set-Content -Path $outputFile -Value $code
        Write-Host "Generated code for: $outputFile"
    } catch {
        Write-Host "Error generating code for $outputFile : $_"
    }
}

# Generate code for each file
foreach ($file in $filePrompts.Keys) {
    $fullPath = Join-Path $projectRoot $file
    if (Test-Path $fullPath) {
        Invoke-Ollama -prompt $filePrompts[$file] -outputFile $fullPath
    } else {
        Write-Host "File not found: $fullPath. Run create_files.ps1 first."
    }
}

Write-Host "Code generation complete. Run deploy_project.ps1 next."