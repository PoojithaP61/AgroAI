# AgroAI Backend Setup Script for Windows PowerShell
# Run this script from the project root directory

Write-Host "🚀 Setting up AgroAI Backend..." -ForegroundColor Green

# Step 1: Navigate to project root
$projectRoot = "C:\Users\pooji\OneDrive\Desktop\AgroAI_FinalYear_Project"
Set-Location $projectRoot
Write-Host "✅ Current directory: $(Get-Location)" -ForegroundColor Cyan

# Step 2: Activate virtual environment
Write-Host "`n📦 Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path "finalenv\Scripts\Activate.ps1") {
    & "finalenv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found at finalenv\Scripts\Activate.ps1" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv finalenv
    & "finalenv\Scripts\Activate.ps1"
}

# Step 3: Upgrade pip
Write-Host "`n⬆️  Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Step 4: Install dependencies
Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Step 5: Verify installation
Write-Host "`n🔍 Verifying installation..." -ForegroundColor Yellow
python -c "import fastapi; import uvicorn; import sqlalchemy; import jose; print('✅ All core dependencies installed')"

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Run: python backend/start.py" -ForegroundColor White
Write-Host "   2. Or: uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
Write-Host "   3. Visit: http://localhost:8000/docs" -ForegroundColor White
