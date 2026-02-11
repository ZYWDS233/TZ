# 批量为所有HTML文件添加nav.js引用的PowerShell脚本

$rootDir = '.'
$processed = 0
$skipped = 0
$errors = 0

Write-Host "开始批量添加导航引用..."

# 递归获取所有HTML文件
$htmlFiles = Get-ChildItem -Path $rootDir -Recurse -Include *.html, *.htm | Where-Object { $_.FullName -notlike "*\.files\*" -and $_.Name -ne "nav.html" }

foreach ($file in $htmlFiles) {
    try {
        # 读取文件内容
        $content = Get-Content -Path $file.FullName -Encoding UTF8 -Raw
        
        # 计算nav.js的相对路径
        $relativePath = $file.Directory.FullName.Replace($PSScriptRoot, "").Trim('\')
        if ($relativePath -eq "") {
            $navJsPath = "nav.js"
        } else {
            $upLevels = ($relativePath -split '\\').Count
            $navJsPath = "../" * $upLevels + "nav.js"
        }
        
        # 检查是否已经添加了nav.js引用
        if ($content -like "*<script src=`"$navJsPath`"></script>*") {
            Write-Host "跳过: $($file.FullName) (已添加)"
            $skipped++
            continue
        }
        
        # 查找</head>标签
        if ($content -like "*</head>*") {
            # 在</head>前添加script标签
            $newContent = $content -replace '</head>', "<script src=`"$navJsPath`"></script></head>"
            
            # 写入修改后的内容
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
            
            Write-Host "成功: $($file.FullName)"
            $processed++
        } else {
            Write-Host "跳过: $($file.FullName) (无</head>标签)"
            $skipped++
        }
    } catch {
        Write-Host "错误: $($file.FullName) - $($_.Exception.Message)"
        $errors++
    }
}

Write-Host "\n处理完成!"
Write-Host "成功处理: $processed 个文件"
Write-Host "跳过: $skipped 个文件"
Write-Host "错误: $errors 个文件"
