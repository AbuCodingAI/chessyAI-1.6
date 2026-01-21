# Copy important files to github_ready folder

$targetFolder = "github_ready"

# Create target folder
New-Item -ItemType Directory -Path $targetFolder -Force | Out-Null

# Core files
$coreFiles = @(
    "index.html",
    "script.js",
    "style.css",
    "server.js",
    "simple-ai.js",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    ".gitignore"
)

# Chocker files
$chockerFiles = @(
    "chocker-demo.js",
    "chocker-launcher.js",
    "chocker-redirect.html",
    "chocker-warnings.js"
)

# Batch files
$batchFiles = @(
    "START_CHESSY_1.4.bat",
    "batch files\open-site.bat"
)

# Neural AI files
$neuralFiles = @(
    "neural-ai\chocker.py",
    "neural-ai\chessy_1.4.py",
    "neural-ai\chess_engine_quiescence.py",
    "neural-ai\chess_engine_deep_search.py",
    "neural-ai\chess_ai_server.py",
    "neural-ai\TRAIN_CHESSY_1.3_IMPROVED.py",
    "neural-ai\test_quiescence.py",
    "neural-ai\start_server.bat"
)

# Combine all files
$allFiles = $coreFiles + $chockerFiles + $batchFiles + $neuralFiles

Write-Host "Copying important files to $targetFolder..." -ForegroundColor Cyan

foreach ($file in $allFiles) {
    if (Test-Path $file) {
        $targetPath = Join-Path $targetFolder $file
        $targetDir = Split-Path $targetPath -Parent
        
        # Create directory if needed
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        
        # Copy file
        Copy-Item -Path $file -Destination $targetPath -Force
        Write-Host "  Copied: $file" -ForegroundColor Green
    } else {
        Write-Host "  Skipped (not found): $file" -ForegroundColor Yellow
    }
}

Write-Host "`nDone! Files copied to $targetFolder" -ForegroundColor Cyan
