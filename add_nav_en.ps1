# PowerShell script to add nav.js reference to all HTML files

$rootDir = '.'
$processed = 0
$skipped = 0
$errors = 0

Write-Host "Starting to add navigation references..."

# Get all HTML files recursively
$htmlFiles = Get-ChildItem -Path $rootDir -Recurse -Include *.html, *.htm | Where-Object { $_.FullName -notlike "*\.files\*" -and $_.Name -ne "nav.html" }

foreach ($file in $htmlFiles) {
    try {
        # Read file content
        $content = Get-Content -Path $file.FullName -Encoding UTF8 -Raw
        
        # Calculate relative path to nav.js
        $relativePath = $file.Directory.FullName.Replace($PSScriptRoot, "").Trim('\')
        if ($relativePath -eq "") {
            $navJsPath = "nav.js"
        } else {
            $upLevels = ($relativePath -split '\\').Count
            $navJsPath = "../" * $upLevels + "nav.js"
        }
        
        # Check if nav.js reference already exists
        if ($content -like "*<script src=`"$navJsPath`"></script>*") {
            Write-Host "Skipped: $($file.FullName) (already added)"
            $skipped++
            continue
        }
        
        # Find </head> tag
        if ($content -like "*</head>*") {
            # Add script tag before </head>
            $newContent = $content -replace '</head>', "<script src=`"$navJsPath`"></script></head>"
            
            # Write modified content back
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
            
            Write-Host "Success: $($file.FullName)"
            $processed++
        } else {
            Write-Host "Skipped: $($file.FullName) (no </head> tag)"
            $skipped++
        }
    } catch {
        Write-Host "Error: $($file.FullName) - $($_.Exception.Message)"
        $errors++
    }
}

Write-Host "\nProcessing completed!"
Write-Host "Successfully processed: $processed files"
Write-Host "Skipped: $skipped files"
Write-Host "Errors: $errors files"
