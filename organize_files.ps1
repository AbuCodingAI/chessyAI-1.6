# Simple script to organize files into repository folders

$batchSize = 100
$folderIndex = 1
$fileList = @()

# Get all files, exclude .md, .log, node_modules, __pycache__, .h5, backups
Get-ChildItem -Recurse -File | Where-Object {
    $_.Extension -ne '.md' -and
    $_.Extension -ne '.log' -and
    $_.Extension -ne '.h5' -and
    $_.FullName -notmatch 'node_modules' -and
    $_.FullName -notmatch '__pycache__' -and
    $_.FullName -notmatch 'backups' -and
    $_.FullName -notmatch '\.git' -and
    $_.FullName -notmatch 'ToBeDeleted' -and
    $_.FullName -notmatch 'repository_folder'
} | ForEach-Object {
    $fileList += $_
}

Write-Host "Found $($fileList.Count) files to organize"

# Organize into batches
for ($i = 0; $i -lt $fileList.Count; $i += $batchSize) {
    $folderName = "repository_folder_$folderIndex"
    $batch = $fileList[$i..[Math]::Min($i + $batchSize - 1, $fileList.Count - 1)]
    
    Write-Host "Creating $folderName with $($batch.Count) files..."
    
    New-Item -ItemType Directory -Path $folderName -Force | Out-Null
    
    foreach ($file in $batch) {
        $relativePath = $file.FullName.Replace((Get-Location).Path + '\', '')
        $targetPath = Join-Path $folderName $relativePath
        $targetDir = Split-Path $targetPath -Parent
        
        New-Item -ItemType Directory -Path $targetDir -Force -ErrorAction SilentlyContinue | Out-Null
        Copy-Item $file.FullName -Destination $targetPath -Force
    }
    
    $folderIndex++
}

Write-Host "Done! Created $($folderIndex - 1) folders"
