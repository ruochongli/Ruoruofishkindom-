# AGENTS.md — 若若的钓鱼王国 (Burst Fishing Kingdom)

> 本文件面向 AI 编码助手。阅读本文件后再修改代码。

---

## 1. 项目概述

- **引擎**：Unity 2022.3 LTS（唯一活跃引擎）
- **语言**：C#（运行时脚本）、Python（工具脚本）
- **平台**：Steam Standalone (Windows/macOS/Linux)
- **类型**：2D 横版 Live2D 动态立绘 + 场景探索
- **规模**：Solo 开发者

---

## 2. 目录约定

```
FishingMaiden/
├── unity_project/           ← 唯一需要写代码的地方
│   └── Assets/_Project/
│       ├── Scripts/         ← C# 代码
│       ├── Scenes/          ← Unity 场景
│       ├── Sprites/         ← 2D 美术资源
│       ├── Data/            ← ScriptableObject 资产
│       ├── Prefabs/         ← 预制体
│       ├── Fonts/           ← TMP 字体
│       └── Audio/           ← 音频
├── docs/                    ← GDD、数据schema、美术规划
├── reference/               ← 美术参考（只读，不要改）
├── tools/                   ← Python 工具脚本
├── archive/                 ← 归档（Godot/HTML 原型，不要碰）
└── README.md / AGENTS.md
```

**禁止把新代码写到 `archive/`、`reference/`、`docs/` 里。**

---

## 3. 代码规范

### 命名空间
所有脚本必须使用命名空间：
```csharp
namespace BurstFishingKingdom.Core { }
namespace BurstFishingKingdom.Player { }
namespace BurstFishingKingdom.Battle { }
namespace BurstFishingKingdom.Inventory { }
namespace BurstFishingKingdom.Equipment { }
namespace BurstFishingKingdom.Crafting { }
namespace BurstFishingKingdom.NPC { }
namespace BurstFishingKingdom.UI { }
```

### 命名约定
| 类型 | 约定 | 示例 |
|---|---|---|
| 类/结构体 | PascalCase | `GameManager`, `PlayerData` |
| 方法 | PascalCase | `LoadScene()`, `AddGold()` |
| 字段（public） | PascalCase | `CurrentState`, `PlayerName` |
| 字段（private） | _camelCase | `_savePath`, `_isDirty` |
| 常量 | UPPER_SNAKE_CASE | `MAX_OFFLINE_HOURS` |
| 枚举 | PascalCase + 前缀区分 | `GameState`, `EquipmentSlot` |
| 事件 | On + PascalCase | `OnGoldChanged`, `OnLevelUp` |

### MonoBehaviour 脚本模板
```csharp
using UnityEngine;

namespace BurstFishingKingdom.XXX
{
    /// <summary>
    /// 一句话说明这个脚本是干什么的
    /// </summary>
    public class MySystem : MonoBehaviour
    {
        // 公开字段用 [Header] 分组
        [Header("配置")]
        [SerializeField] private int _maxItems = 10;
        
        // 公开属性
        public int CurrentCount { get; private set; }
        
        // 事件
        public event System.Action<int> OnCountChanged;
        
        private void Awake() { }
        private void Start() { }
        private void OnDestroy() { }
    }
}
```

---

## 4. 架构原则

### 4.1 GameManager 单例是入口
- `GameManager.Instance` 是全局访问点
- 负责场景切换、游戏状态管理、全局数据引用
- 继承 `MonoBehaviour`，挂在一个 DontDestroyOnLoad 的 GameObject 上

### 4.2 子系统通过 GameManager 暴露
```csharp
GameManager.Instance.PlayerData
GameManager.Instance.SaveManager
GameManager.Instance.TimeManager
```

### 4.3 PlayerData 是玩家状态的中心存储
- 玩家数据（金币、等级、羞耻值、婚姻状态等）存在 `PlayerData`
- `PlayerData` 提供 `ToSaveData()` / `LoadFromSaveData()` 接口
- 外观、装备、背包通过 `GetComponent` 关联

### 4.4 ScriptableObject 做静态数据
- NPC、物品、BOSS、服装的定义用 SO
- 放在 `Assets/_Project/Data/` 下
- 不要在运行时修改 SO 实例（它们是资产，不是存档）

### 4.5 事件驱动解耦
- 优先用 C# `event Action<T>` 做系统间通信
- 避免直接 `FindObjectOfType`（Bootstrap 场景初始化除外）
- 跨系统广播考虑用统一的事件总线（如 `GameEventBus`）

---

## 5. 场景约定

| 场景 | 用途 |
|---|---|
| `00_Bootstrap` | 初始化 GameManager、Player，跳转到主菜单或船舱 |
| `01_ShipCabin` | 船舱：床、衣橱、AI制衣台、出海/进城按钮 |
| `02_City` | 城市：NPC 交互、商店、房产、返回船舱 |
| `03_Sea` | 海域：航行、钓鱼、战斗、返航 |

场景切换统一走：`GameManager.Instance.LoadScene(GameScene.XXX)`

---

## 6. 存档规范

- 存档格式：JSON（`PlayerSaveData` 结构）
- 路径：`Application.persistentDataPath + "/save.json"`
- 保存时机：退出游戏、切后台、手动保存
- 加载时机：Bootstrap 初始化时自动尝试加载
- 版本兼容：存档数据加 `Version` 字段，升级时做数据迁移

---

## 7. 资源导入规范

### Sprite 设置
- Texture Type: **Sprite (2D and UI)**
- Pixels Per Unit: **100**
- Filter Mode: **Point (no filter)** — 像素风
- Compression: 视平台而定，PC 用 **None** 或 **Normal Quality**

### 文件夹命名
- 全小写 + 下划线：`bg_cabin.png`, `sprite_f_stage1.png`
- 避免中文文件名

---

## 8. 提交规范

做改动后，用 `git add` + `git commit` 提交：
```bash
git add -A
git commit -m "type: 简短描述"
```

**type 前缀：**
- `feat:` 新功能
- `fix:` 修复 bug
- `refactor:` 重构
- `art:` 美术资源
- `docs:` 文档
- `chore:` 杂项/工具

**不要修改 `archive/` 里的内容。** 如果确实需要回退到历史原型，单独 checkout 旧分支即可。

---

## 9. 常见禁忌

| ❌ 不要做 | ✅ 应该做 |
|---|---|
| 在 `archive/` 里写新代码 | 只在 `unity_project/Assets/_Project/` 里写 |
| 直接删 `reference/` 里的图 | 把需要的图复制到 `Sprites/` 再用 |
| 运行时修改 ScriptableObject | 用 PlayerData / 本地变量存储动态数据 |
| 用 `FindObjectOfType` 到处查对象 | 在 Bootstrap 初始化后通过 GameManager 引用 |
| 把业务逻辑写在 UI 脚本里 | UI 脚本只负责显示，调用 Manager 做业务 |
| 在 Update 里频繁存档 | 只在状态变化时标记 dirty，退出/切后台时统一存 |

---

## 10. 调试

Play Mode 快捷键（已内置于部分系统）：
- `G` — +100 金币
- `E` — +50 经验
- `T` — 推进 1 小时
- `B` — 直接触发战斗

日志统一用 `Debug.Log("[SystemName] message")` 格式，方便过滤。
