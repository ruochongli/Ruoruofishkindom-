# Image Generation — 哥特二次元立绘生成

## 概述

本项目使用 **ComfyUI + 本地模型** 生成游戏所需的角色立绘美术资源。针对 **NVIDIA RTX 5070 8GB 显存** 优化，主打克鲁鲁/弗洛洛/水银灯风格的哥特华丽二次元美少女。

## 快速开始

### 1. 安装 ComfyUI（首次）

```powershell
# PowerShell 管理员
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\tools\comfyui\setup_comfyui.ps1
```

### 2. 下载模型

```powershell
.\tools\comfyui\download_models.ps1
```

> 模型较大（~4GB），首次下载需要等待。也可用浏览器手动下载后放入对应目录。

### 3. 启动并生成

```powershell
cd $env:USERPROFILE\ComfyUI
python main.py --lowvram --fp16-vae
```

浏览器打开 http://127.0.0.1:8188 → Load 工作流 `docs/comfyui_workflow_gothic_anime.json` → 修改提示词 → Queue Prompt

## 推荐模型

| 模型 | 用途 | 路径 |
|---|---|---|
| Counterfeit-V3.0_fp16 | 哥特/吸血鬼/华丽风格首选 | `models/checkpoints/` |
| meinaMix_V11 | 通用高质量二次元 | `models/checkpoints/` |
| vae-ft-mse-840000 | 色彩VAE | `models/vae/` |

## 提示词模板

### 克鲁鲁风格
```
masterpiece, best quality, ultra-detailed, 8k uhd,
1girl, solo, full body, pale skin, slender, long legs,
platinum blonde hair, long wavy hair, side-swept bangs,
crimson red eyes, slit pupils, sharp gaze, haughty expression,
black military uniform, red cape, high collar, gold trim,
golden crown, vampire fangs, roses, thorns, blood moon background,
dramatic lighting, red rim light, cinematic composition
```

### 弗洛洛风格
```
masterpiece, best quality, ultra-detailed, 8k uhd,
1girl, solo, full body, pale skin, slender, long legs,
black hair, long straight hair, hime cut, red gradient tips,
dark red eyes, mysterious gaze, calm expression, enigmatic smile,
red gothic lolita dress, black lace trim, frilled sleeves,
black ribbon choker, red gemstone, black garter belt, lace stockings,
small black horns, rose hair ornament, ruined cathedral background,
stained glass, candlelight, dramatic lighting, volumetric fog
```

### 水银灯风格
```
masterpiece, best quality, ultra-detailed, 8k uhd,
1girl, solo, full body, pure white skin, snow white, doll joints,
silver white hair, long straight hair, messy bangs,
bright red eyes, no eye highlights, empty gaze, cold expression,
white gothic lolita dress, black ribbon trim, black corset,
black feathered wings, black rose, broken glass,
dark void background, spotlight, floating feathers,
dramatic lighting, high contrast, melancholic atmosphere
```

### 负面提示词
```
lowres, bad anatomy, bad hands, text, error, missing fingers,
extra digit, fewer digits, cropped, worst quality, low quality,
normal quality, jpeg artifacts, signature, watermark, username,
blurry, bad feet, mutation, deformed, extra limbs, extra arms,
extra legs, malformed limbs, fused fingers, too many fingers,
long neck, cross-eyed, mutated hands, polar lowres, bad face,
out of frame, oversaturated, overexposed
```

## 参数速查

| 参数 | SD1.5 | SDXL |
|---|---|---|
| 分辨率 | 512×768 | 832×1216 |
| Steps | 25-30 | 25-30 |
| CFG | 7-9 | 5-7 |
| Sampler | DPM++ 2M Karras | DPM++ 2M Karras |
| Clip Skip | 2 | 1-2 |

## 生成后处理

1. **高清修复**: 使用 ComfyUI Upscale 节点 2x 放大
2. **背景分离**: 用 remove.bg 或 Photoshop 抠图
3. **分层导出**: 身体/服装/头发/配饰分别保存，供 Live2D/Spine 使用
4. **破损阶段**: 同一角色生成 `_full` / `_damaged` / `_broken` / `_destroyed` 四版

## 目录结构

```
FishingMaiden/
├── docs/
│   ├── AIArtGuide.md              ← 完整生成指南
│   └── comfyui_workflow_gothic_anime.json  ← 工作流
├── tools/
│   └── comfyui/
│       ├── setup_comfyui.ps1      ← 安装脚本
│       └── download_models.ps1    ← 模型下载
└── .kimi/skills/image-gen/        ← 本 Skill
```

## 参考资源

- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **Counterfeit-V3.0**: https://huggingface.co/gsdf/Counterfeit-V3.0
- **MeinaMix**: https://huggingface.co/meina/meinaMix_V11
- **Civitai LoRA**: https://civitai.com (搜索 gothic lolita / vampire)
- **Danbooru标签**: https://danbooru.donmai.us
