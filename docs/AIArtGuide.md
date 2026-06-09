# AI 美术生成指南 — 爆衣钓鱼王国

> **目标硬件**: NVIDIA RTX 5070 Laptop 8GB  
> **生成风格**: 哥特/华丽/冷艳二次元美少女立绘  
> **参考角色**: 克鲁鲁·采佩西（终结的炽天使）、弗洛洛（鸣潮）、水银灯（蔷薇少女）

---

## 1. 风格定义

### 1.1 核心视觉特征

| 特征 | 克鲁鲁风格 | 弗洛洛风格 | 水银灯风格 |
|---|---|---|---|
| **主色调** | 黑+红+白 | 黑+红+银白 | 纯白+黑+银灰 |
| **眼睛** | 血红竖瞳，狭长锐利 | 暗红/深紫，神秘深邃 | 纯红无高光，空洞冷冽 |
| **发色** | 淡金/白金长卷发 | 黑长直/暗红渐变 | 银白长直发 |
| **服装** | 黑色军服+红色披风+皇冠 | 红色哥特连衣裙+蕾丝 | 白色哥特裙+黑色丝带+翅膀 |
| **气质** | 高傲女王，吸血鬼神性 | 神秘反派，优雅危险 | 孤独人偶，清冷病娇 |
| **肤色** | 极致苍白，近乎透明 | 苍白微粉 | 雪白无血色 |

### 1.2 共同风格标签

- **哥特洛丽塔** (Gothic Lolita)
- **吸血鬼美学** (Vampire Aesthetic)
- **蔷薇/玫瑰元素** (Roses, Thorns)
- **蕾丝、褶皱、蝴蝶结** (Lace, Frills, Ribbons)
- **皇冠/头饰/角** (Crown, Headpiece, Horns)
- **红黑配色** (Black & Red Color Scheme)
- **高傲/冷漠表情** (Haughty, Cold Expression)
- **纤细身材，长腿** (Slender, Long Legs)
- **红色眼睛** (Red Eyes, Heterochromia)

---

## 2. 推荐模型

### 2.1 主模型 (Checkpoint)

| 模型 | 类型 | 大小 | 特点 | 推荐指数 |
|---|---|---|---|---|
| **Counterfeit-V3.0 fp16** | SD 1.5 | ~4GB | 日式华丽画风，最适合吸血鬼/哥特主题，细节极精致 | ⭐⭐⭐⭐⭐ |
| **MeinaMix V11** | SD 1.5 | ~4GB | 通用高质量二次元，人物稳定，五官端正 | ⭐⭐⭐⭐ |
| **Pony Diffusion V6 XL** | SDXL | ~6GB | 泛用性极强，理解自然语言好，但8GB需 `--lowvram` | ⭐⭐⭐⭐ |

> **8GB显存建议**: 日常使用 Counterfeit-V3.0（SD1.5），速度快且稳定。需要更高分辨率时换 Pony/SDXL。

### 2.2 VAE (色彩解码器)

- **vae-ft-mse-840000-ema-pruned** — 通用最佳VAE，色彩鲜艳不灰

### 2.3 LoRA (风格强化)

| LoRA | 用途 |
|---|---|
| Gothic Lolita Style | 强化哥特服装细节 |
| Vampire Queen / Krul Tepes | 强化吸血鬼女王气质 |
| Red Eyes / Heterochromia | 确保红色眼睛表现 |
| Lace Detail | 强化蕾丝质感 |

---

## 3. 提示词模板

### 3.1 基础立绘模板 (正面全身)

```
masterpiece, best quality, ultra-detailed, 8k uhd,
1girl, solo, full body,
pale skin, slender, long legs,
[发色] hair, [发型], [眼睛] eyes, [表情],
[服装描述],
[配饰描述],
[背景描述],
looking at viewer, standing pose,
dramatic lighting, rim light,
```

### 3.2 克鲁鲁·采佩西风

```
masterpiece, best quality, ultra-detailed, 8k uhd,
1girl, solo, full body,
pale skin, slender, long legs, petite body,
platinum blonde hair, long wavy hair, side-swept bangs,
crimson red eyes, slit pupils, sharp gaze, haughty expression, slight smirk,
black military uniform, red cape, high collar, gold trim,
red ribbon, black thighhighs, red boots,
golden crown, vampire fangs,
roses, thorns, blood moon background,
dramatic lighting, red rim light, cinematic composition,
```

### 3.3 弗洛洛风 (鸣潮风格)

```
masterpiece, best quality, ultra-detailed, 8k uhd,
1girl, solo, full body,
pale skin, slender, long legs,
black hair, long straight hair, hime cut, red gradient tips,
dark red eyes, mysterious gaze, calm expression, enigmatic smile,
red gothic lolita dress, black lace trim, frilled sleeves, off-shoulder,
black ribbon choker, red gemstone, black garter belt, lace stockings,
small black horns, rose hair ornament,
ruined cathedral background, stained glass, candlelight,
dramatic lighting, volumetric fog,
```

### 3.4 水银灯风 (蔷薇少女)

```
masterpiece, best quality, ultra-detailed, 8k uhd,
1girl, solo, full body,
pure white skin, snow white, doll joints, slender fragile body,
silver white hair, long straight hair, messy bangs,
bright red eyes, no eye highlights, empty gaze, cold expression,
white gothic lolita dress, black ribbon trim, black corset,
black feathered wings, black rose, broken glass,
dark void background, spotlight, floating feathers,
dramatic lighting, high contrast, melancholic atmosphere,
```

### 3.5 负面提示词 (通用)

```
lowres, bad anatomy, bad hands, text, error, missing fingers,
extra digit, fewer digits, cropped, worst quality, low quality,
normal quality, jpeg artifacts, signature, watermark, username,
blurry, bad feet, mutation, deformed, extra limbs, extra arms,
extra legs, malformed limbs, fused fingers, too many fingers,
long neck, cross-eyed, mutated hands, polar lowres, bad face,
out of frame, oversaturated, overexposed,
```

进阶负面 (SD1.5 用 EasyNegative + badhandv4):
```
EasyNegative, badhandv4, (worst quality, low quality:1.4),
```

---

## 4. 参数设置

### 4.1 SD 1.5 (Counterfeit / MeinaMix)

| 参数 | 推荐值 | 说明 |
|---|---|---|
| 分辨率 | 512×768 或 512×1024 | SD1.5原生分辨率，512宽最稳定 |
| 采样步数 | 25-30 | DPM++ 2M Karras |
| CFG Scale | 7-9 | 7为安全值，9强化风格 |
| Sampler | DPM++ 2M Karras | 速度质量平衡最佳 |
| Clip Skip | 2 | 二次元模型标准设置 |
| VAE | 840000 VAE | 外挂VAE避免灰图 |
| 高清修复 | 2x, 降噪0.4-0.5 | 先出512×768再放大到1024×1536 |

### 4.2 SDXL (Pony V6)

| 参数 | 推荐值 |
|---|---|
| 分辨率 | 832×1216 (竖版立绘) |
| 采样步数 | 25-30 |
| CFG Scale | 5-7 (Pony对CFG敏感，太高会崩) |
| Sampler | DPM++ 2M Karras / Euler a |
| Refiner | 可用可不用 |

---

## 5. 角色拆分策略 (用于游戏)

由于游戏需要Live2D/Spine动态立绘，建议按以下层次分别生成：

### 5.1 分层生成计划

```
Layer 0: 基础人体 (身体+肤色)
Layer 1: 内衣/基础衣物 (不会被外套遮挡的部分)
Layer 2: 主服装 (连衣裙/外套/披风)
Layer 3: 配饰 (皇冠/丝带/宝石/武器)
Layer 4: 头发前层 (刘海/前发)
Layer 5: 特效 (翅膀/光效/粒子)
```

### 5.2 爆衣系统美术资源生成

每件衣服需要生成 **3个破损阶段**：

| 阶段 | 命名 | 描述 |
|---|---|---|
| Stage 0 | `_full` | 完整服装 |
| Stage 1 | `_damaged` | 轻微破损，裂口+走光边缘 |
| Stage 2 | `_broken` | 严重破损，大面积暴露 |
| Stage 3 | `_destroyed` | 完全破损，仅剩残片 |

**提示词技巧**: 在完整版提示词后追加破损描述：
```
...完整服装描述...,
torn clothes, ripped dress, exposed skin, fabric tear,
```

> ⚠️ **Steam合规**: 确保所有生成内容符合平台规范。建议生成时使用布料遮挡关键部位，或后续用代码层叠加遮挡。

---

## 6. 批量生成脚本 (Python)

当需要生成多个NPC时，可以使用以下脚本批量出图：

```python
# tools/batch_generate.py
# 需要安装: pip install requests

import json
import requests
import time
import os

COMFYUI_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = "../godot_project/assets/characters"

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = requests.post(f"{COMFYUI_URL}/prompt", data=data)
    return req.json()

def generate_character(name, prompt, negative, width=512, height=768, seed=-1):
    """加载工作流JSON并替换提示词后提交"""
    with open("comfyui_workflow_gothic_anime.json", "r", encoding="utf-8") as f:
        workflow = json.load(f)
    
    # 查找并修改KSampler节点的输入
    for node_id, node in workflow.items():
        if node["class_type"] == "KSampler":
            node["inputs"]["seed"] = seed if seed != -1 else int(time.time())
        if node["class_type"] == "CLIPTextEncode":
            if "positive" in str(node).lower() or node_id.endswith("_pos"):
                node["inputs"]["text"] = prompt
            else:
                node["inputs"]["text"] = negative
        if node["class_type"] == "EmptyLatentImage":
            node["inputs"]["width"] = width
            node["inputs"]["height"] = height
    
    result = queue_prompt(workflow)
    print(f"✅ {name} 已提交，Prompt ID: {result.get('prompt_id', 'N/A')}")
    return result

# ========== NPC列表 ==========
CHARACTERS = [
    {
        "name": "lily_portrait",
        "prompt": "masterpiece, best quality, 1girl, solo, full body, ...",
        "negative": "lowres, bad anatomy, ...",
    },
    # 添加更多角色...
]

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for char in CHARACTERS:
        generate_character(char["name"], char["prompt"], char["negative"])
        time.sleep(2)  # 避免队列拥塞
```

---

## 7. 快速启动命令

### 7.1 启动 ComfyUI

```powershell
# 进入ComfyUI目录
cd ~\ComfyUI

# SD1.5 模式 (推荐日常)
python main.py --lowvram --fp16-vae --normalvram

# SDXL 模式 (需要更高质量时)
python main.py --lowvram --fp16-vae

# 如果显存吃紧，加 --cpu-vae
python main.py --lowvram --fp16-vae --cpu-vae
```

### 7.2 浏览器访问

打开 http://127.0.0.1:8188

点击 **Load** 加载工作流 JSON → 修改提示词 → 点击 **Queue Prompt**

---

## 8. 资源链接

| 资源 | 链接 |
|---|---|
| ComfyUI GitHub | https://github.com/comfyanonymous/ComfyUI |
| Counterfeit-V3.0 | https://huggingface.co/gsdf/Counterfeit-V3.0 |
| MeinaMix V11 | https://huggingface.co/meina/meinaMix_V11 |
| Pony Diffusion V6 | https://huggingface.co/AbyssOrangeMix2/ponyDiffusionV6 |
| VAE 840000 | https://huggingface.co/stabilityai/sd-vae-ft-mse-original |
| Civitai LoRA | https://civitai.com (搜索 gothic lolita, vampire, red eyes) |
| 提示词参考 | https://danbooru.donmai.us (标签搜索) |

---

## 9. 立绘质量标准

| 检查项 | 要求 |
|---|---|
| 分辨率 | 至少 1024×1536 (高清修复后) |
| 背景 | 透明/纯色/可分离，方便游戏合成 |
| 比例 | 头身比 1:7 ~ 1:8，符合二次元审美 |
| 表情 | 提供 3-5 种表情差分 |
| 服装 | 同角色提供 3-4 套可换装 |
| 手部 | 重点检查，AI最容易崩的部位 |
| 眼睛 | 必须清晰，红色要有层次感 |

---

*本指南随项目迭代更新。生成的美术资源版权归创作者所有，使用模型时请遵守各模型的许可协议。*
