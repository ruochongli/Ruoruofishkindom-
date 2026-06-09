extends Node
class_name BattleManager

signal turn_started(turn_num: int)
signal player_attacked(damage: int)
signal boss_attacked(target_part: String, wear_amount: int)
signal skill_triggered(skill_name: String, description: String)
signal clothes_state_changed(slot: String, part: String, new_state: String)
signal shame_changed(new_shame: int)
signal battle_ended(victory: bool, drops: Array)
signal log_message(text: String)

var player: GameData.Character
var boss: GameData.Boss
var turn_count: int = 0
var is_battling: bool = false

var active_skill_ids: Array = []
var total_damage_dealt: int = 0

func start_battle(p: GameData.Character, b: GameData.Boss):
    player = p
    boss = b
    turn_count = 0
    is_battling = true
    total_damage_dealt = 0
    active_skill_ids = []
    _emit_log("遭遇了 %s！战斗开始！" % boss.name)
    _update_shame()
    await get_tree().create_timer(1.0).timeout
    _next_turn()

func _next_turn():
    if not is_battling:
        return
    turn_count += 1
    turn_started.emit(turn_count)
    _emit_log("--- 第 %d 回合 ---" % turn_count)

    # BOSS 攻击阶段
    await _boss_attack()
    if not is_battling:
        return

    # 更新羞耻值和技能
    _update_shame()

    # 玩家反击阶段
    await _player_attack()
    if not is_battling:
        return

    # 检查胜利
    if boss.hp <= 0:
        _end_battle(true)
        return

    # 下一回合
    await get_tree().create_timer(1.2).timeout
    _next_turn()

func _boss_attack():
    # 随机选择攻击部位
    var parts = ["top", "bottom", "legs", "accessory"]
    var target_part = parts[randi() % parts.size()]

    # 计算磨损（受玩家防御减免）
    var base_wear = randi_range(20, 50)
    var defense = player.calculate_defense()
    var actual_wear = max(base_wear - defense, 5)

    # 找到该部位对应的装备并扣耐久
    var damaged_slot = ""
    for slot in player.equipped:
        var item = player.equipped[slot]
        if item != null and item.current_durability.has(target_part):
            var real_damage = item.take_damage(target_part, actual_wear)
            if real_damage > 0:
                damaged_slot = slot
                var new_state = item.get_damage_state(target_part)
                clothes_state_changed.emit(slot, target_part, new_state)
                _emit_log("%s 的 %s 受到 %d 点磨损！（剩余 %d/%d）" % [
                    item.name, _part_name(target_part), real_damage,
                    item.current_durability[target_part], item.max_durability[target_part]
                ])
            break

    if damaged_slot == "":
        _emit_log("BOSS 攻击了 %s，但该部位没有装备！" % _part_name(target_part))

    boss_attacked.emit(target_part, actual_wear)
    await get_tree().create_timer(0.8).timeout

func _player_attack():
    var base_dmg = player.base_attack
    var multiplier = 1.0
    var defense_ignore = 0.0

    # 应用羞耻技能
    for skill_id in active_skill_ids:
        var skill = GameData.SKILLS[skill_id]
        if skill["effect_type"] == "damage_boost":
            multiplier += skill["effect_value"]
            _emit_log("【%s】发动！伤害提升 %.0f%%！" % [skill["name"], skill["effect_value"] * 100])
        elif skill["effect_type"] == "defense_ignore":
            defense_ignore += skill["effect_value"]
            _emit_log("【%s】发动！无视 %.0f%% 防御！" % [skill["name"], skill["effect_value"] * 100])

    var effective_defense = int(boss.defense * (1.0 - defense_ignore))
    var damage = int(base_dmg * multiplier) - effective_defense
    damage = max(damage, 1)

    boss.hp = max(0, boss.hp - damage)
    total_damage_dealt += damage

    player_attacked.emit(damage)
    _emit_log("艾莉造成 %d 点伤害！BOSS 剩余 HP: %d/%d" % [damage, boss.hp, boss.max_hp])
    await get_tree().create_timer(0.5).timeout

func _update_shame():
    var old_shame = player.shame
    player.shame = player.calculate_shame()

    if player.shame != old_shame:
        shame_changed.emit(player.shame)
        _emit_log("羞耻值变化: %d → %d" % [old_shame, player.shame])

    # 检测新触发的技能
    var new_skills = player.get_active_skills()
    for skill_id in new_skills:
        if not active_skill_ids.has(skill_id):
            active_skill_ids.append(skill_id)
            var skill = GameData.SKILLS[skill_id]
            skill_triggered.emit(skill["name"], skill["description"])
            _emit_log("★ 羞耻技能解锁: %s！" % skill["name"])

func _end_battle(victory: bool):
    is_battling = false
    var drops = []
    if victory:
        _emit_log("胜利！击败了 %s！" % boss.name)
        drops = _calculate_drops()
        for drop in drops:
            _emit_log("获得: %s x%d" % [drop["item_id"], drop["amount"]])
    battle_ended.emit(victory, drops)

func _calculate_drops() -> Array:
    var result = []
    var rng = RandomNumberGenerator.new()
    rng.randomize()
    for entry in boss.drop_table:
        if randf() <= entry["chance"]:
            var amount = randi_range(entry["min"], entry["max"])
            result.append({"item_id": entry["item_id"], "amount": amount})
    return result

func _part_name(part: String) -> String:
    match part:
        "top": return "上衣"
        "bottom": return "裙子"
        "legs": return "袜子"
        "accessory": return "配饰"
    return part

func _emit_log(text: String):
    log_message.emit(text)
    print(text)

func stop_battle():
    is_battling = false
