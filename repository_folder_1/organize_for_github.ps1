# PowerShell script to organize files into repository folders
# Excludes .md files, .log files, and anything in .gitignore

$sourceDir = Get-Location
$batchSize = 100
$folderIndex = 1

# Read .gitignore patterns
$gitignorePatterns = @()
if (Test-Path ".gitignore") {
    $gitignorePatterns = Get-Content ".gitignore" | Where-Object { 
        $_ -notmatch '^\s*#' -and $_ -notmatch '^\s*$' 
    }
}

# Function to check if file should be ignored
function Should-Ignore {
    param($filePath)
    
    $fileName = Split-Path $filePath -Leaf
    $relativePath = $filePath.Replace($sourceDir.Path + "\", "")
    
    # Ignore .md files
    if ($fileName -match '\.md$') { return $true }
    
    # Ignore .log files
    if ($fileName -match '\.log$') { return $true }
    
    # Check gitignore patterns
    foreach ($pattern in $gitignorePatterns) {
        $pattern = $pattern.Trim()
        
        # Handle directory patterns
        if ($pattern -match '/$') {
            $dirPattern = $pattern.TrimEnd('/')
            if ($relativePath -match "^$dirPattern" -or $relativePath -match "\\$dirPattern") {
                return $true
            }
        }
        # Handle wildcard patterns
        elseif ($pattern -match '\*') {
            $regexPattern = $pattern -replace '\*', '.*' -replace '\.', '\.'
            if ($relativePath -match $regexPattern -or $fileName -match $regexPattern) {
                return $true
            }
        }
        # Handle exact matches
        else {
            if ($relativePath -match $pattern -or $fileName -eq $pattern) {
                return $true
            }
        }
    }
    
    return $false
}

# Get all files recursively, excluding ignored ones
Write-Host "Scanning files..." -ForegroundColor Cyan
$allFiles = Get-ChildItem -Path $sourceDir -Recurse -File | Where-Object {
    -not (Should-Ignore $_.FullName)
}

Write-Host "Found $($allFiles.Count) files to organize" -ForegroundColor Green

# Organize files into batches
$fileIndex = 0
$currentBatch = @()

foreach ($file in $allFiles) {
    $currentBatch += $file
    $fileIndex++
    
    # When batch is full or last file
    if ($currentBatch.Count -eq $batchSize -or $fileIndex -eq $allFiles.Count) {
        $folderName = "repository_folder_$folderIndex"
        $targetFolder = Join-Path $sourceDir $folderName
        
        # Create folder
        if (-not (Test-Path $targetFolder)) {
            New-Item -ItemType Directory -Path $targetFolder | Out-Null
        }
        
        Write-Host "`nCopying to $folderName ($($currentBatch.Count) files)..." -ForegroundColor Yellow
        
        # Copy files maintaining structure
        foreach ($file in $currentBatch) {
            $relativePath = $file.FullName.Replace($sourceDir.Path + "\", "")
            $targetPath = Join-Path $targetFolder $relativePath
            $targetDir = Split-Path $targetPath -Parent
            
            # Create directory structure
            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            }
            
            # Copy file
            Copy-Item -Path $file.FullName -Destination $targetPath -Force
            Write-Host "  Copied: $relativePath" -ForegroundColor Gray
        }
        
        Write-Host "✓ $folderName complete!" -ForegroundColor Green
        
        # Reset for next batch
        $currentBatch = @()
        $folderIndex++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Organization Complete!" -ForegroundColor Green
Write-Host "Created $($folderIndex - 1) repository folders" -ForegroundColor Green
Write-Host "Total files organized: $fileIndex" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
