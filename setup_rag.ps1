# RAG Setup Script - Phase 2 Week 3
# Run this to setup the RAG (Retrieval Augmented Generation) system

Write-Host ">>> Setting up RAG System for AiKO..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Docker
Write-Host "[Step 1] Checking Docker..." -ForegroundColor Yellow
$dockerRunning = docker ps 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Docker is not running! Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Docker is running" -ForegroundColor Green
Write-Host ""

# Step 2: Start services
Write-Host "[Step 2] Starting Docker services (PostgreSQL + Qdrant)..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to start Docker services!" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Services started" -ForegroundColor Green
Write-Host ""

# Wait for Qdrant to be ready
Write-Host "[Wait] Waiting for Qdrant to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
$qdrantReady = $false
for ($i = 1; $i -le 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:6333/" -UseBasicParsing -TimeoutSec 2 2>$null
        if ($response.StatusCode -eq 200) {
            $qdrantReady = $true
            break
        }
    } catch {
        # Retry
    }
    Start-Sleep -Seconds 2
}

if ($qdrantReady) {
    Write-Host "[OK] Qdrant is ready!" -ForegroundColor Green
} else {
    Write-Host "[WARN] Qdrant might still be starting up..." -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Check .env file
Write-Host "[Step 3] Checking .env configuration..." -ForegroundColor Yellow
$envPath = "backend\.env"
$envExamplePath = "backend\.env.example"

if (!(Test-Path $envPath)) {
    Write-Host "[WARN] .env file not found. Creating from .env.example..." -ForegroundColor Yellow
    Copy-Item $envExamplePath $envPath
    Write-Host "[OK] Created .env file" -ForegroundColor Green
    Write-Host ""
    Write-Host "[IMPORTANT] Please update backend\.env with your actual values:" -ForegroundColor Red
    Write-Host "   - GEMINI_API_KEY=your_actual_api_key" -ForegroundColor Yellow
    Write-Host "   - DATABASE_URL (check if correct)" -ForegroundColor Yellow
    Write-Host ""
} else {
    # Check if Qdrant config exists
    $envContent = Get-Content $envPath -Raw
    if ($envContent -notmatch "QDRANT_HOST") {
        Write-Host "[WARN] Adding Qdrant configuration to .env..." -ForegroundColor Yellow
        Add-Content $envPath "`n# Qdrant Vector Database"
        Add-Content $envPath "QDRANT_HOST=localhost"
        Add-Content $envPath "QDRANT_PORT=6333"
        Add-Content $envPath "QDRANT_COLLECTION_NAME=aiko_memories"
        Add-Content $envPath "`n# RAG Configuration"
        Add-Content $envPath "EMBEDDING_MODEL=all-MiniLM-L6-v2"
        Add-Content $envPath "MEMORY_SEARCH_LIMIT=5"
        Add-Content $envPath "MEMORY_RELEVANCE_THRESHOLD=0.7"
        Write-Host "[OK] Added Qdrant configuration to .env" -ForegroundColor Green
    } else {
        Write-Host "[OK] .env file configured" -ForegroundColor Green
    }
}
Write-Host ""

# Step 4: Install dependencies
Write-Host "[Step 4] Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "[Wait] This may take 2-5 minutes (downloading torch ~1GB)..." -ForegroundColor Yellow
Push-Location backend
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location
Write-Host "[OK] Dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 5: Show services status
Write-Host "[Step 5] Checking services..." -ForegroundColor Yellow
Write-Host ""
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Select-String -Pattern "aiko"
Write-Host ""

# Summary
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "[SUCCESS] RAG SETUP COMPLETE!" -ForegroundColor Green
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services Running:" -ForegroundColor Yellow
Write-Host "   - PostgreSQL    -> localhost:5432" -ForegroundColor White
Write-Host "   - Qdrant        -> http://localhost:6333" -ForegroundColor White
Write-Host "   - Qdrant UI     -> http://localhost:6333/dashboard" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Start server:" -ForegroundColor White
Write-Host "      cd backend" -ForegroundColor Cyan
Write-Host "      python -m app.main" -ForegroundColor Cyan
Write-Host ""
Write-Host "   2. Open test interface:" -ForegroundColor White
Write-Host "      http://localhost:8000/test-chat" -ForegroundColor Cyan
Write-Host ""
Write-Host "   3. Test RAG system:" -ForegroundColor White
Write-Host "      python scripts/test_rag.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "   backend\PHASE2_WEEK3_RAG.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "[TIP] First run will download embedding model (~90MB)" -ForegroundColor Yellow
Write-Host "===============================================================" -ForegroundColor Cyan
