# 若若的钓鱼王国 - ComfyUI 安装脚本
# 针对 RTX 5070 8GB 显存优化
# 运行: 右键 -> 使用 PowerShell 运行

$ErrorActionPreference = "Stop"
$ComfyDir = "$env:USERPROFILE\ComfyUI"
$ModelsDir = "$ComfyDir\models\checkpoints"
$VaeDir = "$ComfyDir\models\vae"
$LoraDir = "$ComfyDir\models\loras"
$WorkflowDir = "$ComfyDir\user\default\workflows"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ComfyUI 安装器 - 若若的钓鱼王国专用" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host "❌ 未找到 Python。请先安装 Python 3.10+ (推荐 3.10.11)" -ForegroundColor Red
    Write-Host "   下载地址: https://www.python.org/downloads/release/python-31011/" -ForegroundColor Yellow
    exit 1
}

python --version
Write-Host ""

# 克隆 ComfyUI
if (Test-Path $ComfyDir) {
    Write-Host "⚠️ ComfyUI 目录已存在: $ComfyDir" -ForegroundColor Yellow
    $confirm = Read-Host "是否重新安装? (y/N)"
    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        Remove-Item -Recurse -Force $ComfyDir
    } else {
        Write-Host "跳过克隆，直接更新依赖..." -ForegroundColor Green
    }
}

if (-not (Test-Path $ComfyDir)) {
    Write-Host "📦 正在克隆 ComfyUI..." -ForegroundColor Cyan
    git clone https://github.com/comfyanonymous/ComfyUI.git $ComfyDir
}

# 安装依赖
Write-Host "📦 正在安装 Python 依赖..." -ForegroundColor Cyan
Set-Location $ComfyDir
python -m pip install -r requirements.txt

# 创建模型目录
New-Item -ItemType Directory -Force -Path $ModelsDir | Out-Null
New-Item -ItemType Directory -Force -Path $VaeDir | Out-Null
New-Item -ItemType Directory -Force -Path $LoraDir | Out-Null
New-Item -ItemType Directory -Force -Path $WorkflowDir | Out-Null

# 复制工作流
$ProjectWorkflow = "$PSScriptRoot\..\..\docs\comfyui_workflow_gothic_anime.json"
if (Test-Path $ProjectWorkflow) {
    Copy-Item $ProjectWorkflow "$WorkflowDir\gothic_anime_portrait.json" -Force
    Write-Host "✅ 已复制工作流到 ComfyUI" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ComfyUI 安装完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📂 安装路径: $ComfyDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "  1. 运行下载模型脚本: .\download_models.ps1" -ForegroundColor White
Write-Host "  2. 启动 ComfyUI: python main.py --lowvram --fp16-vae" -ForegroundColor White
Write-Host "  3. 浏览器打开: http://127.0.0.1:8188" -ForegroundColor White
Write-Host ""
Write-Host "💡 8GB显存推荐启动参数:" -ForegroundColor Yellow
Write-Host "   python main.py --lowvram --fp16-vae --normalvram (SD1.5模型)" -ForegroundColor Gray
Write-Host "   python main.py --lowvram --fp16-vae (SDXL模型)" -ForegroundColor Gray
Write-Host ""

Set-Location $PSScriptRoot
