extends Node2D

# ============================
# 主场景脚本 - 简化版原型入口
# ============================

@onready var battle_manager = BattleManager.new()

# 当前角色和BOSS
var player: GameData.Character
var current_boss: GameData.Boss

func _ready():
    # 初始化随机种子
    randomize()

    # 创建玩家
    player = GameData.Character.new()
    player.name = "艾莉"
    player.base_attack = 20

    # 初始装备默认连衣裙（可在UI中切换）
    _equip_clothes("summer_dress")

    # 连接战斗信号（可在此处理UI更新）
    battle_manager.skill_triggered.connect(_on_skill_triggered)
    battle_manager.battle_ended.connect(_on_battle_ended)
    battle_manager.log_message.connect(_on_log_message)

    print("游戏初始化完成。调用 start_fishing_battle() 开始一场战斗。")

func _equip_clothes(cloth_id: String):
    var dress = GameData.ClothingItem.new(cloth_id)
    player.equip("top", dress)
    player.equip("bottom", dress)
    player.equip("legs", dress)
    if dress.max_durability.has("accessory"):
        player.equip("accessory", dress)
    print("已装备: %s" % dress.name)

func start_fishing_battle():
    # 创建BOSS
    current_boss = GameData.Boss.new("abyss_carp")
    print("遭遇 BOSS: %s (HP: %d)" % [current_boss.name, current_boss.max_hp])

    # 开始战斗
    battle_manager.start_battle(player, current_boss)

func switch_clothes(cloth_id: String):
    _equip_clothes(cloth_id)

# 信号回调
func _on_skill_triggered(skill_name: String, description: String):
    print("[技能触发] %s: %s" % [skill_name, description])

func _on_battle_ended(victory: bool, drops: Array):
    if victory:
        print("战斗胜利！获得掉落:")
        for drop in drops:
            print("  - %s x%d" % [drop["item_id"], drop["amount"]])
    else:
        print("战斗结束。")

func _on_log_message(text: String):
    # 这里可以连接到UI的RichTextLabel
    pass
