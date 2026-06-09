# 数据结构文档

## 1. PlayerProfile（玩家档案）

```gdscript
class_name PlayerProfile

var player_name: String = "冒险者"
var gender: int = Gender.FEMALE
var appearance: AppearanceData

var level: int = 1
var exp: int = 0
var gold: int = 0

var equipped: Dictionary = {"top": null, "bottom": null, "legs": null, "accessory": null}
var base_attack: int = 20
var base_charm: int = 10
var shame: int = 0
var active_skill_ids: Array[String] = []

var npc_favor: Dictionary = {}
var npc_relationship: Dictionary = {}

var inventory: Inventory
var current_city_id: String = "breeze_harbor"
var current_ship_id: String = "ship_001"
var owned_houses: Dictionary = {}
var owned_ships: Array[String] = ["ship_001"]

# 婚姻状态
var spouse_npc_id: String = ""
var wedding_date: String = ""
var is_divorced: bool = false
var marriage_days: int = 0   # 已婚天数，影响船员能力

# 船员状态
var active_crew_id: String = ""   # 当前同行的NPC船员ID（空=独行）
var crew_equipment: Dictionary = {}   # npc_id -> rod_id

# 制衣系统
var saved_recipes: Array[Recipe] = []
var recipe_book: Dictionary = {}
var crafting_level: int = 1

# 每日商店
var last_shop_refresh_day: int = 0
var shop_refresh_count: int = 0

func _init():
    appearance = AppearanceData.new()
    inventory = Inventory.new()
```

### RelationshipStage

```gdscript
enum RelationshipStage {
    STRANGER = 0, ACQUAINTANCE = 1, FRIENDLY = 2,
    INTIMATE = 3, LOVER = 4, ENGAGED = 5, MARRIED = 6
}
```

---

## 2. AppearanceData

```gdscript
class_name AppearanceData

var skin_tone: int = 2          // 创角时自选，默认白皙偏粉
var face_shape: int = 0
var hair_style: int = 0         // 创角时自选，见 ArtPlan.md 发型表
var hair_color: Color           // 创角时自选（16色），无硬编码默认值
var eye_style: int = 0
var eye_color: Color            // 创角时自选（16色），无硬编码默认值
var eyebrow_style: int = 0
var mouth_style: int = 0

func to_dict() -> Dictionary:
    return {
        "skin_tone": skin_tone, "face_shape": face_shape,
        "hair_style": hair_style, "hair_color": hair_color.to_html(),
        "eye_style": eye_style, "eye_color": eye_color.to_html(),
        "eyebrow_style": eyebrow_style, "mouth_style": mouth_style,
    }

static func from_dict(d: Dictionary) -> AppearanceData:
    var a = AppearanceData.new()
    a.skin_tone = d.get("skin_tone", 2)
    a.face_shape = d.get("face_shape", 0)
    a.hair_style = d.get("hair_style", 0)
    a.hair_color = Color(d.get("hair_color", "#5c3a21"))
    a.eye_style = d.get("eye_style", 0)
    a.eye_color = Color(d.get("eye_color", "#3b82f6"))
    a.eyebrow_style = d.get("eyebrow_style", 0)
    a.mouth_style = d.get("mouth_style", 0)
    return a
```

---

## 3. ItemQuality（道具品质系统）

```gdscript
class_name ItemQuality

enum Quality { COMMON = 0, UNCOMMON = 1, RARE = 2, EPIC = 3, LEGENDARY = 4, MYTHIC = 5 }

const QUALITY_NAMES: Array[String] = ["普通", "优质", "稀有", "史诗", "传说", "神话"]
const QUALITY_COLORS: Array[Color] = [
    Color("#e2e8f0"), Color("#4ade80"), Color("#3b82f6"),
    Color("#a855f7"), Color("#f97316"), Color("#facc15")
]
const QUALITY_STARS: Array[int] = [1, 2, 3, 4, 5, 6]

static func get_name(q: int) -> String: return QUALITY_NAMES[q]
static func get_color(q: int) -> Color: return QUALITY_COLORS[q]
static func get_stars(q: int) -> int: return QUALITY_STARS[q]

static func get_durability_multiplier(q: int) -> float:
    match q: 0: return 1.0; 1: return 1.2; 2: return 1.5; 3: return 2.0; 4: return 3.0; 5: return 4.0
    return 1.0

static func get_defense_bonus(q: int) -> int:
    match q: 0: return 0; 1: return 5; 2: return 15; 3: return 30; 4: return 50; 5: return 80
    return 0
```

---

## 4. Item（道具基类）

```gdscript
class_name Item

var id: String
var name: String
var description: String
var category: String
var quality: int = 0
var icon: String
var max_stack: int = 99
var material_type: String = ""
var obtain_methods: Array[Dictionary] = []
```

---

## 5. Dye（染料）

```gdscript
class_name Dye
extends Item

var color_name: String
var color_hex: String

static func get_dye_source(color: String) -> Dictionary:
    match color:
        "red": return { "name": "红色花卉染剂", "sources": [{"type":"plant","item":"red_rose","amount":3},{"type":"shop","price":50}] }
        "blue": return { "name": "蓝色海藻染剂", "sources": [{"type":"gather","location":"mid_sea","item":"blue_seaweed","amount":3},{"type":"shop","price":80}] }
        "black": return { "name": "黑色墨鱼汁", "sources": [{"type":"fish","target":"squid","amount":1}] }
        "white": return { "name": "白色贝壳粉", "sources": [{"type":"gather","location":"beach","item":"seashell","amount":5},{"type":"shop","price":30}] }
        "purple": return { "name": "紫色曼陀罗染剂", "sources": [{"type":"plant","item":"purple_mandrake","amount":2},{"type":"shop","price":300}], "rare": true }
        "gold": return { "name": "金色龙血染剂", "sources": [{"type":"boss_drop","target":"golden_dragon","chance":0.5}], "rare": true }
    return {}
```

---

## 6. Recipe / AIRecipe（配方）

```gdscript
class_name Recipe

var id: String
var name: String
var description: String
var input_text: String
var output_cloth_id: String
var output_quality: int
var output_cloth_name: String
var materials: Array[RecipeMaterial] = []
var required_crafting_level: int = 1
var required_workbench_level: int = 1
var is_unlocked: bool = false
var is_completed: bool = false

class RecipeMaterial:
    var item_id: String
    var item_name: String
    var required_amount: int
    var current_amount: int = 0
    var quality_required: int = 0
    var is_optional: bool = false
    var obtain_hint: String = ""
```

---

## 7. DailyShop（每日商店）

```gdscript
class_name DailyShop

var shop_id: String
var shop_name: String
var shop_type: String
var city_id: String
var refresh_hour: int = 6
var items: Array[ShopItem] = []
var last_refresh_day: int = 0
var manual_refresh_cost: int = 100
var manual_refresh_multiplier: float = 2.0
var max_manual_refresh: int = 10
var today_refresh_count: int = 0

class ShopItem:
    var item_id: String
    var item_name: String
    var quality: int
    var amount: int
    var price: int
    var is_limited: bool = false
    var limited_stock: int = -1
    var discount: float = 1.0
    func get_display_price() -> int: return int(price * discount)
```

---

## 8. NPC（非玩家角色）

```gdscript
class_name NPC

var id: String
var name: String
var gender: String = "female"
var home_city_id: String
var sexuality: String = "bi"
var shame_reaction_type: String = "concern"

var appearance: AppearanceData
var default_outfit_id: String
var current_outfit_id: String
var npc_wardrobe: Array[String] = []

var favor: int = 0
var max_favor: int = 200
var relationship_stage: int = RelationshipStage.STRANGER
var is_dating_player: bool = false
var is_engaged_to_player: bool = false
var is_married_to_player: bool = false

var schedule: NPCSchedule
var dialogues: Array[NPCDialogue] = []
var personal_quests: Array[String] = []
var romance_events: Array[RomanceEvent] = []

var gift_preferences: NPCGiftPreferences
var favorite_date_locations: Array[String] = []
var favorite_proposal_scene: String = "beach"

# === NPC船员战斗数据 ===
var combat_data: NPCCombatData

func is_romanceable_by(player_gender: int) -> bool:
    match sexuality:
        "hetero": return (gender == "female" and player_gender == Gender.MALE) or (gender == "male" and player_gender == Gender.FEMALE)
        "homo": return (gender == "female" and player_gender == Gender.FEMALE) or (gender == "male" and player_gender == Gender.MALE)
        "bi", "pan", "player_only": return true
    return false
```

### NPCCombatData（NPC战斗数据）

```gdscript
class_name NPCCombatData

# NPC类型决定基础定位
enum CrewType { SUPPORT, FIGHTER, BURST, STABLE }

var crew_type: int = CrewType.SUPPORT
var base_dps: int = 10           # 每回合基础伤害
var crit_chance: float = 0.0     # 暴击率
var crit_multiplier: float = 2.0 # 暴击倍率
var heal_amount: int = 0         # 每回合治疗量（ Support型）
var heal_chance: float = 0.0     # 治疗触发概率

# 战斗中台词
var battle_start_lines: Array[String] = []
var player_shame_lines: Array[String] = []     # 主角爆衣时
var player_skill_lines: Array[String] = []     # 主角触发技能时
var victory_lines: Array[String] = []
var repair_lines: Array[String] = []           # 战后修补时

# 修补能力
var base_repair_percent: float = 0.15   # 基础修补百分比（0.15=15%）
var repair_priority: String = "most_damaged"   # most_damaged / even / random
var can_combat_repair: bool = false     # 灵魂伴侣阶段：战斗中低概率紧急修补
var combat_repair_chance: float = 0.05
var combat_repair_amount: float = 0.10

# 计算当前DPS（根据婚姻天数加成）
func calculate_current_dps(marriage_days: int) -> int:
    var multiplier = 1.0
    if marriage_days >= 180: multiplier = 2.0
    elif marriage_days >= 90: multiplier = 1.5
    elif marriage_days >= 30: multiplier = 1.2
    return int(base_dps * multiplier)

# 计算当前修补量
func calculate_current_repair(marriage_days: int) -> float:
    var multiplier = 1.0
    if marriage_days >= 180: multiplier = 2.0
    elif marriage_days >= 90: multiplier = 1.6
    elif marriage_days >= 30: multiplier = 1.3
    return min(base_repair_percent * multiplier, 0.5)   # 最高50%
```

### NPCSchedule（NPC日程）

```gdscript
class_name NPCSchedule

var daily_schedule: Array[TimeSlot] = []
var weather_override: Dictionary = {}
var season_override: Dictionary = {}

class TimeSlot:
    var start_hour: int
    var end_hour: int
    var location_id: String
    var activity: String
    var is_sleeping: bool = false
    var interactable: bool = true
    var romance_bonus: bool = false
```

### NPCGiftPreferences

```gdscript
class_name NPCGiftPreferences

var liked_categories: Dictionary = {}
var disliked_categories: Dictionary = {}
var favorite_items: Array[String] = []
var hated_items: Array[String] = []
var liked_clothing_styles: Array[String] = []

func calculate_favor_bonus(item_id: String, item_category: String, item_style: String = "") -> int:
    var base = 10
    if favorite_items.has(item_id): return 50
    if hated_items.has(item_id): return -20
    if liked_categories.has(item_category): base *= liked_categories[item_category]
    if disliked_categories.has(item_category): base *= disliked_categories[item_category]
    if liked_clothing_styles.has(item_style): base *= 1.5
    return int(base)
```

### RomanceEvent

```gdscript
class_name RomanceEvent

var event_id: String
var required_stage: int
var required_favor: int
var trigger_condition: String
var event_type: String
var dialogue_lines: Array[NPCDialogue] = []
var choices: Array[DialogueChoice] = []
var next_event_id: String = ""
var favor_change: int = 0
var unlock_outfit_id: String = ""
var unlock_recipe_id: String = ""
```

---

## 9. City（城市）

```gdscript
class_name City

var id: String
var name: String
var description: String
var climate: String
var theme_color: Color
var unlock_condition: Dictionary = {}
var has_market: bool = true
var has_shipyard: bool = true
var has_realty: bool = true
var has_tavern: bool = false
var has_chapel: bool = false
var available_houses: Array[HouseTemplate] = []
var resident_npcs: Array[String] = []
var connected_seas: Array[String] = []
var local_specialties: Array[String] = []
var locations: Dictionary = {}

class Location:
    var id: String
    var name: String
    var type: String
    var npc_capacity: int = 5
```

---

## 10. House / HouseTemplate（房产）

```gdscript
class_name HouseTemplate

var id: String
var name: String
var description: String
var city_id: String
var level: int
var price: int
var grid_size: Vector2i
var max_furniture: int
var built_in_facilities: Array[String] = []
```

```gdscript
class_name OwnedHouse

var template_id: String
var nickname: String = ""
var placed_furniture: Dictionary = {}
var wallpaper_id: String = "default"
var floor_id: String = "default"
var is_primary_home: bool = false
var daily_yield: Dictionary = {}
var residents: Array[String] = []
```

---

## 11. Ship / ShipTemplate（船只）

```gdscript
class_name ShipTemplate

var id: String
var name: String
var description: String
var level: int
var price: int
var grid_size: Vector2i
var max_sea_level: int = 1
var sailing_speed: float = 1.0
var cargo_capacity: int = 20
var exterior_sprite: String
var interior_sprite: String
```

```gdscript
class_name OwnedShip

var template_id: String
var nickname: String = ""
var placed_facilities: Dictionary = {}
var docked_city_id: String = "breeze_harbor"
var durability: int = 100
var is_favorite: bool = false
var expedition_loadout: ExpeditionLoadout
var onboard_npcs: Array[String] = []
```

---

## 12. ClothingItem（衣服物品）

```gdscript
class_name ClothingItem

var id: String
var name: String
var description: String
var gender_tag: String = "unisex"
var has_npc_version: bool = false
var npc_version_sprite: Dictionary = {}
var max_durability: Dictionary
var current_durability: Dictionary
var sprite_layers: Dictionary
var defense: int = 0
var special_skill_id: String = ""
var craft_cost: Dictionary
var dyeable: bool = false
var dye_color: Color = Color.WHITE
var style_tags: Array[String] = []

var quality: int = 0
var max_durability_bonus: float = 1.0
var defense_bonus: int = 0
var shame_skill_count: int = 0
var visual_effect: String = ""

func get_durability_ratio(part: String) -> float:
    if not max_durability.has(part) or max_durability[part] == 0: return 1.0
    return float(current_durability[part]) / float(max_durability[part])

func take_damage(part: String, amount: int) -> int:
    if not current_durability.has(part): return 0
    var before = current_durability[part]
    current_durability[part] = max(0, current_durability[part] - amount)
    return before - current_durability[part]

func apply_quality(quality_level: int):
    quality = quality_level
    max_durability_bonus = ItemQuality.get_durability_multiplier(quality_level)
    defense_bonus = ItemQuality.get_defense_bonus(quality_level)
    match quality_level:
        0, 1: shame_skill_count = 0
        2: shame_skill_count = 1
        3: shame_skill_count = 2
        4, 5: shame_skill_count = 3
```

---

## 13. BattleState（战斗状态 - 含NPC）

```gdscript
class_name BattleState

enum Phase { IDLE, FISHING, ENCOUNTER, BOSS_TURN, PLAYER_TURN, VICTORY, DEFEAT, RETREAT }

var phase: Phase = Phase.IDLE
var current_boss: Boss
var player: PlayerProfile
var turn_count: int = 0
var battle_log: Array[String] = []

# NPC船员（如果有）
var active_crew: NPC = null          # 当前同行的NPC
var crew_damage_dealt: int = 0       # NPC累计伤害

# 伤害计算（主角）
func calculate_player_damage() -> int:
    var base = player.base_attack
    var bonus = 1.0
    var ignore_def = 0.0
    for skill_id in player.active_skill_ids:
        var skill = GameDatabase.get_skill(skill_id)
        match skill.effect_type:
            "damage_boost": bonus += skill.effect_value
            "defense_ignore": ignore_def += skill.effect_value
    var effective_def = int(current_boss.defense * (1.0 - ignore_def))
    return max(int(base * bonus) - effective_def, 1)

# NPC每回合伤害
func calculate_crew_damage() -> int:
    if active_crew == null or active_crew.combat_data == null: return 0
    var dps = active_crew.combat_data.calculate_current_dps(player.marriage_days)
    # 暴击判定
    var is_crit = randf() < active_crew.combat_data.crit_chance
    if is_crit: dps = int(dps * active_crew.combat_data.crit_multiplier)
    return dps

# NPC治疗（Support型）
func calculate_crew_heal() -> int:
    if active_crew == null or active_crew.combat_data == null: return 0
    var cd = active_crew.combat_data
    if cd.heal_amount <= 0: return 0
    if randf() > cd.heal_chance: return 0
    return cd.heal_amount

# 磨损计算
func calculate_wear_damage(target_part: String) -> int:
    var base_wear = randi_range(20, 50)
    var defense = 0
    if player.equipped.has(target_part) and player.equipped[target_part] != null:
        defense = player.equipped[target_part].defense
    return max(base_wear - defense, 5)
```

---

## 14. SaveData（存档结构）

```gdscript
class_name SaveData

var save_version: String = "1.4"
var save_time: String
var play_time_seconds: int = 0

var player: PlayerProfile
var unlocked_cities: Array[String] = ["breeze_harbor"]
var completed_quests: Array[String] = []
var active_quests: Array[Quest] = []

# NPC状态
var npc_states: Dictionary = {}

# 每日商店
var shop_states: Dictionary = {}

# 世界状态
var world_state: Dictionary = {
    "current_date": "Day 1",
    "current_hour": 8,
    "weather": "sunny",
    "season": "spring",
    "city_events": {}
}
```
