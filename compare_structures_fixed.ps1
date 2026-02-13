# 读取天舟.wcp文件
$wcpContent = Get-Content -Path "topics\天舟.wcp" -Encoding UTF8 -Raw

# 提取TitleList信息
$titlePattern = 'TitleList\.Title\.(\d+)=(.*?)\r\n'
$levelPattern = 'TitleList\.Level\.(\d+)=(\d+)\r\n'
$urlPattern = 'TitleList\.Url\.(\d+)=(.*?)\r\n'

$titles = [regex]::Matches($wcpContent, $titlePattern) | ForEach-Object {
    @{
        Index = [int]$_.Groups[1].Value
        Title = $_.Groups[2].Value
    }
}

$levels = [regex]::Matches($wcpContent, $levelPattern) | ForEach-Object {
    @{
        Index = [int]$_.Groups[1].Value
        Level = [int]$_.Groups[2].Value
    }
}

$urls = [regex]::Matches($wcpContent, $urlPattern) | ForEach-Object {
    @{
        Index = [int]$_.Groups[1].Value
        Url = $_.Groups[2].Value
    }
}

# 构建标题字典
$titleDict = @{}
foreach ($title in $titles) {
    $titleDict[$title.Index] = @{
        Title = $title.Title
        Level = 0
        Url = ""
    }
}

# 添加层级信息
foreach ($level in $levels) {
    if ($titleDict.ContainsKey($level.Index)) {
        $titleDict[$level.Index].Level = $level.Level
    }
}

# 添加URL信息
foreach ($url in $urls) {
    if ($titleDict.ContainsKey($url.Index)) {
        $titleDict[$url.Index].Url = $url.Url
    }
}

# 按索引排序
$sortedTitles = $titleDict.GetEnumerator() | Sort-Object Key

# 生成目录结构
$wcpStructure = @()
foreach ($item in $sortedTitles) {
    $level = $item.Value.Level
    $url = $item.Value.Url
    
    # 从URL中提取文件名
    if ($url) {
        $filename = $url.Split('\\')[-1]
    } else {
        $filename = $item.Value.Title
    }
    
    # 生成缩进
    $indent = '    ' * $level
    
    # 添加到结构中
    $wcpStructure += "$indent$filename"
}

# 保存到文件
$wcpStructure | Out-File -FilePath "wcp_directory_structure.txt" -Encoding UTF8
Write-Host "WCP文件的目录结构已保存到 wcp_directory_structure.txt"

# 读取目录结构.txt文件
$txtStructure = Get-Content -Path "目录结构.txt" -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }
Write-Host "目录结构.txt中有 $($txtStructure.Count) 个条目"

# 对比两个结构
Write-Host "\n对比结果："
Write-Host "WCP文件中有 $($wcpStructure.Count) 个条目"
Write-Host "目录结构.txt中有 $($txtStructure.Count) 个条目"

# 找出差异
$diffFound = $false
$minLength = [Math]::Min($wcpStructure.Count, $txtStructure.Count)

for ($i = 0; $i -lt $minLength; $i++) {
    if ($wcpStructure[$i] -ne $txtStructure[$i]) {
        Write-Host "第 $($i+1) 行不同："
        Write-Host "  WCP: $($wcpStructure[$i])"
        Write-Host "  TXT: $($txtStructure[$i])"
        $diffFound = $true
    }
}

# 检查长度差异
if ($wcpStructure.Count -ne $txtStructure.Count) {
    Write-Host "\n长度不同：WCP有 $($wcpStructure.Count) 行，TXT有 $($txtStructure.Count) 行"
    $diffFound = $true
}

if (-not $diffFound) {
    Write-Host "\n两个文件的目录结构完全相同！"
} else {
    Write-Host "\n已找到差异，请查看详细输出。"
}
