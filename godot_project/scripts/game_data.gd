extends Node
class_name GameData

# ============================
# 若若的钓鱼王国 - 游戏数据配置中心
# ============================

# ===== 性别枚举 =====
enum Gender { MALE, FEMALE }

# ===== 外观数据类 =====
class AppearanceData:
    var skin_tone: int = 2        # 0-5
    var face_shape: int = 0       # 0-3
    var hair_style: int = 0       # 0-7(男) / 0-9(女)
    var hair_color: Color = Color("#5c3a21")
    var eye_style: int = 0        # 0-5
    var eye_color: Color = Color("#3b82f6")
    var eyebrow_style: int = 0    # 0-5
    var mouth_style: int = 0      # 0-3

    func to_dict() -> Dictionary:
        return {
            "skin_tone": skin_tone,
            "face_shape": face_shape,
            "hair_style": hair_style,
            "hair_color": hair_color.to_html(),
            "eye_style": eye_style,
            "eye_color": eye_color.to_html(),
            "eyebrow_style": eyebrow_style,
            "mouth_style": mouth_style,
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

# ===== 玩家档案 =====
class PlayerProfile:
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
    var inventory: Dictionary = {}  # item_id -> count

    func _init():
        appearance = AppearanceData.new()

    func calculate_shame() -> int:
        var total = 0
        for slot in equipped:
            var item = equipped[slot]
            if item == null: continue
            for part in item.current_durability:
                var ratio = item.get_durability_ratio(part)
                var damage = 1.0 - ratio
                total += int(damage * 33)
        return clamp(total, 0, 100)

    func calculate_defense() -> int:
        var total = 0
        for slot in equipped:
            if equipped[slot] != null:
                total += equipped[slot].defense
        return total

    func get_active_skills() -> Array:
        var active = []
        var current_shame = calculate_shame()
        for skill_id in SKILLS:
            var skill = SKILLS[skill_id]
            if _check_condition(skill["condition"], current_shame):
                active.append(skill_id)
        return active

    func _check_condition(condition: String, shame_val: int) -> bool:
        if condition == "shame >= 30": return shame_val >= 30
        if condition == "shame >= 60": return shame_val >= 60
        if condition == "shame >= 90": return shame_val >= 90
        return false

# ===== 衣服定义 =====
const CLOTHES := {
    "novice_cloth": {
        "name": "新手布衣",
        "description": "玛莎阿姨给的基础衣服，结实耐用。",
        "gender_tag": "unisex",
        "max_durability": {"top": 100, "bottom": 100, "legs": 100, "accessory": 50},
        "defense": 15,
        "special_skill": "",
        "layers": {
            "intact": {"male": "", "female": ""},
            "damaged": {"male": "", "female": ""},
            "broken": {"male": "", "female": ""}
        }
    },
    "thin_pajamas": {
        "name": "轻薄睡衣",
        "description": "几乎没有防护，但羞耻值积累极快。",
        "gender_tag": "unisex",
        "max_durability": {"top": 40, "bottom": 40, "legs": 30, "accessory": 0},
        "defense": 0,
        "special_skill": "midnight_bloom",
        "layers": {
            "intact": {"male": "", "female": ""},
            "damaged": {"male": "", "female": ""},
            "broken": {"male": "", "female": ""}
        }
    }
}

# ===== BOSS定义 =====
const BOSSES := {
    "stream_king": {
        "name": "溪流鲤鱼王",
        "hp": 120,
        "attack": 25,
        "defense": 5,
        "drop_table": [
            {"item_id": "carp_scale", "chance": 1.0, "min": 1, "max": 2},
            {"item_id": "rare_fish", "chance": 0.4, "min": 1, "max": 1}
        ]
    },
    "abyss_carp": {
        "name": "深渊鲤鱼",
        "hp": 200,
        "attack": 35,
        "defense": 10,
        "drop_table": [
            {"item_id": "carp_scale", "chance": 1.0, "min": 1, "max": 3},
            {"item_id": "rare_fish", "chance": 0.5, "min": 1, "max": 1},
            {"item_id": "golden_hook", "chance": 0.1, "min": 1, "max": 1}
        ]
    }
}

# ===== 羞耻技能定义 =====
const SKILLS := {
    "panic_counter": {
        "name": "慌乱反击",
        "description": "因为羞耻而爆发出的惊人力量，伤害+40%。",
        "condition": "shame >= 30",
        "effect_type": "damage_boost",
        "effect_value": 0.4
    },
    "armor_break": {
        "name": "破衣解放",
        "description": "抛弃矜持，无视BOSS 30%防御。",
        "condition": "shame >= 60",
        "effect_type": "defense_ignore",
        "effect_value": 0.3
    },
    "limit_bloom": {
        "name": "极限绽放",
        "description": "在极限羞耻中释放全部潜能，伤害翻倍！",
        "condition": "shame >= 90",
        "effect_type": "damage_boost",
        "effect_value": 1.0
    },
    "midnight_bloom": {
        "name": "深夜绽放",
        "description": "【睡衣专属】在破损中散发危险魅力，掉率+30%。",
        "condition": "shame >= 50 and clothing_id == 'thin_pajamas'",
        "effect_type": "drop_boost",
        "effect_value": 0.3
    }
}

# ===== NPC定义 =====
const NPCS := {
    "hein": {
        "name": "海恩",
        "shame_reaction": "tease",
        "romanceable": false,
        "dialogues": [
            {"conditions": ["quest:intro"], "text_m": "哈哈哈！新来的小伙子，欢迎来到宁静港湾村！", "text_f": "哈哈哈！新来的小姑娘，欢迎来到宁静港湾村！"}
        ]
    },
    "martha": {
        "name": "玛莎",
        "shame_reaction": "concern",
        "romanceable": false
    },
    "lily": {
        "name": "莉莉",
        "shame_reaction": "admire",
        "romanceable": true
    }
}

# ===== 衣服物品类 =====
class ClothingItem:
    var id: String
    var name: String
    var description: String
    var gender_tag: String
    var max_durability: Dictionary
    var current_durability: Dictionary
    var defense: int
    var special_skill: String
    var layers: Dictionary

    func _init(data_id: String):
        id = data_id
        var template = GameData.CLOTHES[data_id]
        name = template["name"]
        description = template["description"]
        gender_tag = template["gender_tag"]
        max_durability = template["max_durability"].duplicate()
        current_durability = template["max_durability"].duplicate()
        defense = template["defense"]
        special_skill = template["special_skill"]
        layers = template["layers"].duplicate()

    func get_durability_ratio(part: String) -> float:
        if not max_durability.has(part) or max_durability[part] == 0:
            return 1.0
        return float(current_durability[part]) / float(max_durability[part])

    func take_damage(part: String, amount: int) -> int:
        if not current_durability.has(part):
            return 0
        var before = current_durability[part]
        current_durability[part] = max(0, current_durability[part] - amount)
        return before - current_durability[part]

    func get_damage_state(part: String) -> String:
        var ratio = get_durability_ratio(part)
        if ratio <= 0.0: return "gone"
        if ratio <= 0.25: return "broken"
        if ratio <= 0.5: return "damaged"
        if ratio <= 0.75: return "worn"
        return "intact"

# ===== BOSS类 =====
class Boss:
    var id: String
    var name: String
    var max_hp: int
    var hp: int
    var attack: int
    var defense: int
    var drop_table: Array

    func _init(data_id: String):
        id = data_id
        var template = GameData.BOSSES[data_id]
        name = template["name"]
        max_hp = template["hp"]
        hp = max_hp
        attack = template["attack"]
        defense = template["defense"]
        drop_table = template["drop_table"].duplicate()
