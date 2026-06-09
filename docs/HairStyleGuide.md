# 发型生成指南

> 用于指导 AI 生成剩余 7 种发型素材，确保与已有 3 张风格统一。

---

## 1. 风格统一规范

生成任何发型时必须严格遵守以下设定，否则无法用于创角系统：

| 项目 | 固定值 |
|---|---|
| **角色** | 同一少女（不能换脸/换身材） |
| **姿势** | 正面站立，双手背在身后，双腿微交叉 |
| **服装** | 白色无袖连衣裙（及膝）+ 棕色凉鞋 |
| **眼睛** | 紫罗兰色瞳孔，平静略带冷淡的表情 |
| **肤色** | 白皙偏粉 |
| **分辨率** | 1773 × 2364 px（竖版） |
| **背景** | 纯白色（#FFFFFF） |
| **风格** | 高清像素风 / 伪像素艺术 / anime pixel art |
| **水印** | 可接受右下角小字，后续脚本会自动去除 |

**已有参考图**：
- `myart/初始人物.png` — 黑长直（最标准的基准图）
- `myart/初始角色双马尾.png` — 双马尾
- `myart/初始角色短发.png` — 短发

---

## 2. AI 绘画提示词（Prompt）

### 通用前缀（所有发型共用）

**中文提示词模板**：
```
高清像素风格美少女立绘，正面全身站立姿势，双手背在身后，白色无袖连衣裙，棕色凉鞋，紫罗兰色眼睛，白皙皮肤，平静冷淡表情，纯白色背景，伪像素艺术，anime pixel art，1773x2364，角色设计，游戏立绘
```

**英文提示词模板**：
```
Full body anime girl standing front view, hands behind back, white sleeveless dress, brown sandals, violet eyes, fair skin, calm neutral expression, pure white background, pixel art style, high resolution pixel art, anime pixel art, 1773x2364, character design, game sprite, sharp pixel edges, soft shading
```

---

### 3. 各发型专属提示词

#### ID 3 — 高马尾（Ponytail）

**中文**：
```
黑色长发扎成高马尾，马尾垂至腰际，前额有碎刘海，侧边有几缕发丝垂下，活泼清爽
```

**英文**：
```
black hair in a high ponytail reaching waist level, forehead bangs, side strands framing face, energetic and fresh look
```

#### ID 4 — 丸子头（Bun）

**中文**：
```
黑色头发在头顶两侧扎成两个丸子头（团子头），剩余长发垂至肩部，齐刘海，可爱俏皮
```

**英文**：
```
black hair in double buns on top of head, remaining hair down to shoulders, straight bangs, cute and playful
```

#### ID 5 — 侧马尾（Side Ponytail）

**中文**：
```
黑色长发全部梳向左侧，在左耳下方扎成侧马尾，马尾长及腰，右侧露出脖颈，优雅温柔
```

**英文**：
```
all black hair swept to left side, tied in a low side ponytail below left ear, ponytail reaching waist, right side of neck exposed, elegant and gentle
```

#### ID 6 — 姬发式 / 公主切（Hime Cut）

**中文**：
```
黑色长直发及腰，前额齐刘海，脸颊两侧有整齐的一刀切短鬓角（公主切），后侧长发笔直垂下，古典优雅
```

**英文**：
```
black straight hair to waist, straight bangs, hime cut with cheek-length sidelocks framing face sharply, back hair perfectly straight, classical elegant Japanese beauty
```

#### ID 7 — 卷发 / 大波浪（Wavy）

**中文**：
```
黑色中长发及胸，自然大波浪卷发，发丝蓬松有空气感，侧分刘海，成熟妩媚
```

**英文**：
```
black medium-length wavy hair to chest, loose big curls, airy voluminous hair, side-swept bangs, mature and charming
```

#### ID 8 — 狼尾 / 鲻鱼头（Wolf Cut）

**中文**：
```
黑色层次感短发，顶部蓬松有碎刘海，两侧较短，后颈处留长呈狼尾状，酷帅中性风
```

**英文**：
```
black layered short wolf cut, voluminous top with choppy bangs, shorter sides, longer mullet-like back near nape, cool androgynous style
```

#### ID 9 — 呆毛短发（Ahoge）

**中文**：
```
黑色及肩短发，发尾微翘，头顶有一根标志性呆毛翘起，活泼元气，少年感
```

**英文**：
```
black shoulder-length short hair, slightly flipped ends, one iconic ahoge strand sticking up from crown, energetic and youthful, tomboyish
```

---

## 4. 生成后处理流程

每张新图生成后，按以下步骤处理：

1. **保存到 `myart/` 目录**，命名格式：
   ```
   初始角色[发型名].png
   例如：初始角色高马尾.png
   ```

2. **运行自动抠图脚本**：
   ```powershell
   cd C:\Users\Ruoruo\FishingMaiden
   .\tools\AutoChromaKey.ps1 -InputPath "myart\初始角色高马尾.png" -OutputPath "docs\hair_ponytail.png" -TargetHeight 600 -Tolerance 35
   ```

3. **检查去底效果**：
   - 如果裙子内部出现黑色透明瑕疵（如双马尾图），改用白底原图：
   ```powershell
   # 仅缩放，不去底
   .\tools\AutoChromaKey.ps1 -InputPath "myart\初始角色高马尾.png" -OutputPath "docs\hair_ponytail.png" -TargetHeight 600 -Tolerance 0
   ```
   （注：Tolerance 0 时脚本会跳过 flood fill，只缩放。需要更新脚本支持此模式，或手动用其他工具抠图。）

4. **更新 `ArtPlan.md` 发型表**：将 ⏳ 改为 ✅

---

## 5. 风格一致性检查清单

拿到新图后，对比以下项目确认可用：

- [ ] 是同一张脸（眼睛、嘴型、脸型一致）
- [ ] 是同一套白色连衣裙
- [ ] 是同一双棕色凉鞋
- [ ] 姿势相同（正面站立，双手背后）
- [ ] 分辨率 1773×2364
- [ ] 背景为纯白
- [ ] 像素风格一致
- [ ] 无多余配饰（耳环、项链等会干扰图层拆分）

---

## 6. 快速参考：已有素材状态

| 素材 | 状态 | 备注 |
|---|---|---|
| 初始人物（黑长直） | ✅ 完美 | 基准图 |
| 初始角色短发 | ✅ 完美 | |
| 初始角色双马尾 | ⚠️ 可用 | 裙内有几处小瑕疵，不明显 |
| 4阶段破损图 | ✅/⚠️ 混合 | Stage2 用白底版，其余透明 |
