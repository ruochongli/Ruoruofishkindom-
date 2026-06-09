# Unity 工程配置指南

## 环境要求
- **Unity 2022.3 LTS** 或更高版本
- **平台**: Windows / macOS / Linux (Standalone)

## 打开项目

1. 打开 **Unity Hub**
2. 点击 **Open** → 选择 `unity_project` 文件夹
3. Unity 会自动解析 Packages 和 ProjectSettings

## 首次打开后的配置步骤

### 1. 场景添加到 Build Settings
打开 `File → Build Settings`，确保以下场景已按顺序添加：
```
0. Assets/_Project/Scenes/00_Bootstrap.unity
1. Assets/_Project/Scenes/01_ShipCabin.unity
2. Assets/_Project/Scenes/02_City.unity
3. Assets/_Project/Scenes/03_Sea.unity
```
（已预设在 EditorBuildSettings.asset 中，Unity 打开后应自动识别）

### 2. 创建 ScriptableObject 数据资产

在 `Assets/_Project/Data/` 下创建以下文件夹结构和资产：

#### NPC 数据 (`Data/NPCs/`)
创建两个 NPCData ScriptableObject：
- `lily.asset` — 莉莉
  - Name: 莉莉
  - Gender: Female
  - Sexuality: Bi
  - HomeCityId: breeze_harbor
  - MaxFavor: 200
  - DailySchedule: 设置 24h 日程
  - CombatData.BaseDPS: 15
  
- `hein.asset` — 海恩
  - Name: 海恩
  - Gender: Male
  - Sexuality: Pan
  - HomeCityId: breeze_harbor
  - MaxFavor: 200
  - CombatData.BaseDPS: 18

#### BOSS 数据 (`Data/Bosses/`)
- `coastal_crab.asset` — 近海巨蟹
- `stream_king.asset` — 溪流鲤鱼王
- `mid_sea_serpent.asset` — 中海海蛇
- `abyss_leviathan.asset` — 深海利维坦

#### 物品数据 (`Data/Items/`)
创建基础材料 ItemSO：
- `fabric.asset` — 丝绸布料
- `thread.asset` — 丝线
- `dye_red.asset` — 红色花卉染剂
- `dye_blue.asset` — 蓝色海藻染剂
- `dye_black.asset` — 黑色墨鱼汁
- `lace.asset` — 蕾丝边
- `ribbon.asset` — 丝带
- `boss_scale.asset` — 海兽鳞片

### 3. 创建 GameManager Prefab

1. 在 Hierarchy 中创建一个空物体，命名为 `GameManager`
2. 添加以下组件：
   - `GameManager`
   - `SaveManager`
   - `TimeManager`
   - `OfflineRewardManager`
   - `DailyShopSystem`
   - `CitySystem`
   - `ShipCabinSystem`
   - `SailingSystem`
   - `RomanceSystem`
   - `CrewSystem`
   - `TalentSystem`
3. 将 `GameManager` 物体拖到 `Assets/_Project/Prefabs/` 保存为 Prefab
4. **删除 Hierarchy 中的实例**（Bootstrap 场景会负责创建）

### 4. 配置 Bootstrap 场景

打开 `00_Bootstrap.unity`：
1. 创建一个空物体，命名为 `Bootstrap`
2. 添加 `GameBootstrap` 脚本
3. 将 `GameManager Prefab` 拖到 `GameManagerPrefab` 字段
4. 勾选 `SkipToGameplay`（如需直接跳转到船舱）
5. 或者创建 UI Canvas，添加 MainMenu 面板

### 5. 配置 Player 预制体

1. 创建空物体 `Player`
2. 添加组件：
   - `PlayerData`
   - `PlayerAppearance`
   - `EquipmentManager`
   - `InventoryGrid`
3. 保存为 `Assets/_Project/Prefabs/Player.prefab`
4. 在 `GameBootstrap` 中配置引用（或让其自动创建）

### 6. 配置 UI Canvas（各场景）

#### ShipCabin 场景
- 创建 Canvas（Screen Space - Overlay）
- 添加面板：
  - 船舱主界面（床、衣橱、AI制衣台按钮）
  - 角色面板（挂接 `CharacterPanelUI`）
  - 出海按钮 → 调用 `SailingSystem.StartSailing()`
  - 进城按钮 → `GameManager.LoadScene(City)`

#### City 场景
- 城市背景
- NPC 交互按钮（莉莉、海恩）
- 商店面板（挂接 `DailyShopSystem`）
- 返回船舱按钮

#### Sea 场景
- 海域背景
- 航行进度条
- 战斗面板（挂接 `BattleManager`）
- 战斗日志 Text 区域
- 返航按钮

### 7. 配置 BattleManager

在 `Sea` 场景中：
1. 创建空物体 `BattleManager`
2. 添加 `BattleManager` 脚本
3. 配置 BOSS 引用（或使用 `SailingSystem.OnBossEncountered` 事件动态设置）

### 8. 字体配置

所有使用了 `TextMeshProUGUI` 的 UI 元素需要：
- 创建或导入中文字体资源（TMP Font Asset）
- 替换所有 TextMeshPro 组件的字体引用

## 已知待完善

- [ ] 美术资源：角色 Sprite、背景、UI 素材
- [ ] Live2D/Spine 集成（如需动态立绘）
- [ ] 音效和背景音乐
- [ ] 完整的 NPC 对话数据
- [ ] 更多海域和 BOSS
- [ ] 船只升级系统 UI
- [ ] 成就系统
- [ ] Steam 集成（存档、成就、云同步）

## 调试快捷键

在 Unity Play Mode 中：
- `G` — 加 100 金币
- `E` — 加 50 经验
- `T` — 推进 1 小时
- `B` — 直接开始战斗（测试用）

## 项目结构

```
unity_project/
├── Packages/
│   ├── manifest.json
│   └── packages-lock.json
├── ProjectSettings/
│   ├── ProjectVersion.txt
│   ├── EditorSettings.asset
│   ├── GraphicsSettings.asset
│   ├── QualitySettings.asset
│   ├── TagManager.asset
│   └── EditorBuildSettings.asset
└── Assets/
    └── _Project/
        ├── Scripts/
        │   ├── Core/          (GameManager, Save, Time, Shop, City, Ship, Sailing, Bootstrap)
        │   ├── Player/        (Data, Appearance, Talent)
        │   ├── Battle/        (Manager, BossData)
        │   ├── Inventory/     (Grid, ItemSO)
        │   ├── Equipment/     (Manager, ClothingSO, Slot)
        │   ├── Crafting/      (AICraftSystem)
        │   ├── NPC/           (Data, Romance, Crew)
        │   └── UI/            (MainMenu, CharacterCreation, CharacterPanel)
        ├── Scenes/
        │   ├── 00_Bootstrap.unity
        │   ├── 01_ShipCabin.unity
        │   ├── 02_City.unity
        │   └── 03_Sea.unity
        ├── Data/              (NPCs, Items, Clothing, Bosses)
        ├── Prefabs/           (GameManager, Player)
        ├── Sprites/           (角色、服装、背景)
        ├── Fonts/             (TMP 中文字体)
        └── Audio/             (BGM、音效)
```
