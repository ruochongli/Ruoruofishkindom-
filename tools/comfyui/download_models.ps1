# 爆衣钓鱼王国 - 二次元模型下载脚本
# 针对 克鲁鲁/弗洛洛/水银灯 风格的哥特华丽美少女

$ErrorActionPreference = "Stop"
$ComfyDir = "$env:USERPROFILE\ComfyUI"
$ModelsDir = "$ComfyDir\models\checkpoints"
$VaeDir = "$ComfyDir\models\vae"
$LoraDir = "$ComfyDir\models\loras"

function Download-File($Url, $OutFile) {
    if (Test-Path $OutFile) {
        Write-Host "✅ 已存在，跳过: $(Split-Path $OutFile -Leaf)" -ForegroundColor Green
        return
    }
    Write-Host "⬇️ 下载: $(Split-Path $OutFile -Leaf)" -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri $Url -OutFile $OutFile -MaximumRedirection 5
        Write-Host "✅ 完成: $(Split-Path $OutFile -Leaf)" -ForegroundColor Green
    } catch {
        Write-Host "❌ 下载失败: $(Split-Path $OutFile -Leaf)" -ForegroundColor Red
        Write-Host "   错误: $_" -ForegroundColor DarkRed
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  二次元模型下载器" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "💾 模型将保存到: $ModelsDir" -ForegroundColor Yellow
Write-Host ""

# 创建目录
New-Item -ItemType Directory -Force -Path $ModelsDir | Out-Null
New-Item -ItemType Directory -Force -Path $VaeDir | Out-Null
New-Item -ItemType Directory -Force -Path $LoraDir | Out-Null

# ======================
# 主模型 (Checkpoint)
# ======================
Write-Host "【主模型 - 必选一款】" -ForegroundColor Magenta

# Counterfeit-V3.0 - 最适合哥特/华丽/吸血鬼风格，日式精细画风
# HuggingFace 镜像下载
Download-File `
    "https://huggingface.co/gsdf/Counterfeit-V3.0/resolve/main/Counterfeit-V3.0_fp16.safetensors" `
    "$ModelsDir\Counterfeit-V3.0_fp16.safetensors"

# MeinaMix V11 - 通用高质量二次元，人物稳定
Download-File `
    "https://huggingface.co/meina/meinaMix_V11/resolve/main/meinaMix_V11.safetensors" `
    "$ModelsDir\meinaMix_V11.safetensors"

# ======================
# VAE (色彩解码器)
# ======================
Write-Host ""
Write-Host "【VAE - 推荐下载】" -ForegroundColor Magenta

# 840000 VAE - 通用高质量VAE，色彩更鲜艳
Download-File `
    "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors" `
    "$VaeDir\vae-ft-mse-840000-ema-pruned.safetensors"

# ======================
# LoRA (风格强化)
# ======================
Write-Host ""
Write-Host "【LoRA - 可选风格强化】" -ForegroundColor Magenta

# 哥特洛丽塔风格 LoRA
# Civitai 需要 API Key 或手动下载，这里提供链接

Write-Host ""
Write-Host "以下 LoRA 需要手动从 Civitai 下载:" -ForegroundColor Yellow
Write-Host "  1. Gothic Lolita Style LoRA" -ForegroundColor White
Write-Host "     https://civitai.com/models/123456/gothic-lolita-style" -ForegroundColor Gray
Write-Host "     (搜索 'gothic lolita lora' 下载排名最高的)" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Vampire Queen Style LoRA" -ForegroundColor White
Write-Host "     (搜索 'vampire queen lora' 或 'krul tepes lora')" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. 红色眼睛/异色瞳 LoRA" -ForegroundColor White
Write-Host "     (搜索 'heterochromia lora' 或 'red eyes lora')" -ForegroundColor Gray
Write-Host ""
Write-Host "下载后放到: $LoraDir" -ForegroundColor Yellow

# ======================
# Embeddings (负面提示词嵌入)
# ======================
Write-Host ""
Write-Host "【Embeddings - 负面提示词优化】" -ForegroundColor Magenta
$EmbDir = "$ComfyDir\models\embeddings"
New-Item -ItemType Directory -Force -Path $EmbDir | Out-Null

Write-Host "推荐下载 (手动):" -ForegroundColor Yellow
Write-Host "  EasyNegative.pt - https://civitai.com/models/7808/easynegative" -ForegroundColor Gray
Write-Host "  badhandv4.pt - https://civitai.com/models/16993/badhandv4" -ForegroundColor Gray
Write-Host "  放到: $EmbDir" -ForegroundColor Yellow

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  下载任务完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📂 模型路径: $ModelsDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 下一步:" -ForegroundColor Yellow
Write-Host "   1. 启动 ComfyUI: python main.py --lowvram --fp16-vae" -ForegroundColor White
Write-Host "   2. 浏览器打开: http://127.0.0.1:8188" -ForegroundColor White
Write-Host "   3. 加载工作流: 点击 'Load' 选择 gothic_anime_portrait.json" -ForegroundColor White
Write-Host "   4. 选择模型: Counterfeit-V3.0_fp16 或 meinaMix_V11" -ForegroundColor White
Write-Host ""
