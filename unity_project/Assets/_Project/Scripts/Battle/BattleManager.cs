using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;

namespace BurstFishingKingdom.Battle
{
    /// <summary>
    /// 战斗管理器
    /// 处理放置自动战斗逻辑、爆衣计算、羞耻技能、NPC船员辅助
    /// </summary>
    public class BattleManager : MonoBehaviour
    {
        public static BattleManager Instance { get; private set; }

        [Header("战斗状态")]
        public BattleState CurrentState = BattleState.Idle;
        public int TurnCount = 0;

        [Header("当前BOSS")]
        public BossData CurrentBoss;

        [Header("战斗日志")]
        public List<string> BattleLog = new();
        public int MaxLogEntries = 50;

        [Header("船员伤害统计")]
        public int CrewTotalDamage = 0;

        public event Action OnBattleStarted;
        public event Action<bool> OnBattleEnded;
        public event Action<string> OnLogAdded;
        public event Action<int> OnTurnChanged;
        public event Action<int> OnShameChanged;
        public event Action<Equipment.EquipmentSlot, int> OnDurabilityChanged;

        private Coroutine _battleCoroutine;
        private Player.PlayerData _playerData;
        private Equipment.EquipmentManager _equipmentManager;
        private NPC.CrewSystem _crewSystem;

        private void Awake()
        {
            if (Instance != null && Instance != this) { Destroy(gameObject); return; }
            Instance = this;
        }

        /// <summary>
        /// 开始战斗
        /// </summary>
        public void StartBattle(BossData boss)
        {
            if (CurrentState != BattleState.Idle) return;

            CurrentBoss = boss;
            CurrentBoss.CurrentHp = CurrentBoss.MaxHp;
            TurnCount = 0;
            CrewTotalDamage = 0;
            BattleLog.Clear();
            CurrentState = BattleState.Battling;

            _playerData = GameManager.Instance.PlayerData;
            _equipmentManager = _playerData.GetComponent<Equipment.EquipmentManager>();
            _crewSystem = FindObjectOfType<NPC.CrewSystem>();

            AddLog($"🚨 遭遇海兽：{boss.BossName}！");
            AddLog($"HP: {boss.MaxHp} | 防御: {boss.Defense} | 攻击: {boss.Attack}");

            if (_crewSystem?.HasActiveCrew() == true)
            {
                var crew = _crewSystem.GetActiveCrew();
                AddLog($"💕 {crew.NPCData.Name} 加入战斗！");
            }

            OnBattleStarted?.Invoke();
            
            // 初始化全身立绘为完整状态
            UpdateFullbodyAppearance();
            
            _battleCoroutine = StartCoroutine(BattleLoop());
        }

        private IEnumerator BattleLoop()
        {
            while (CurrentState == BattleState.Battling && CurrentBoss.CurrentHp > 0)
            {
                yield return new WaitForSeconds(1.5f);
                TurnCount++;
                OnTurnChanged?.Invoke(TurnCount);

                // 1. BOSS攻击
                BossAttack();

                yield return new WaitForSeconds(0.3f);

                // 2. 玩家攻击
                PlayerAttack();

                yield return new WaitForSeconds(0.3f);

                // 3. 船员攻击
                if (_crewSystem?.HasActiveCrew() == true)
                {
                    CrewAttack();
                }

                // 检查胜负
                if (CurrentBoss.CurrentHp <= 0)
                {
                    EndBattle(true);
                    yield break;
                }

                // 检查玩家全灭（可选：全部衣服损坏即失败）
                if (CheckPlayerDefeat())
                {
                    EndBattle(false);
                    yield break;
                }
            }
        }

        private void BossAttack()
        {
            // 随机选择一个外层装备攻击
            var possibleSlots = new List<Equipment.EquipmentSlot> 
            { 
                Equipment.EquipmentSlot.Top, 
                Equipment.EquipmentSlot.Bottom, 
                Equipment.EquipmentSlot.Socks 
            };
            
            var slot = possibleSlots[UnityEngine.Random.Range(0, possibleSlots.Count)];
            var item = _equipmentManager.GetEquipped(slot);
            
            if (item == null) return;

            int baseDamage = UnityEngine.Random.Range(20, 50);
            int defense = item.Defense;
            int actualDamage = Mathf.Max(baseDamage - defense, 5);

            _equipmentManager.TakeDamage(slot, actualDamage);
            
            int currentDur = _equipmentManager.CurrentDurability[slot];
            AddLog($"海兽冲撞！{item.ItemName} 受到 {actualDamage} 磨损（剩余 {currentDur}）");

            // 更新羞耻值
            UpdateShame();

            // 更新全身立绘爆衣状态
            UpdateFullbodyAppearance();
        }

        private void PlayerAttack()
        {
            int baseAttack = _equipmentManager.GetTotalAttack();
            float multiplier = 1f;
            float ignoreDef = 0f;
            List<string> activeSkills = new();

            // 羞耻技能检查
            if (_playerData.Shame >= 30) { multiplier += 0.4f; activeSkills.Add("慌乱反击"); }
            if (_playerData.Shame >= 60) { ignoreDef += 0.3f; activeSkills.Add("破衣解放"); }
            if (_playerData.Shame >= 90) { multiplier += 1.0f; activeSkills.Add("极限绽放"); }

            // 天赋加成
            multiplier *= FindObjectOfType<Player.TalentSystem>()?.GetDamageMultiplier() ?? 1f;

            int effectiveDef = Mathf.FloorToInt(CurrentBoss.Defense * (1f - ignoreDef));
            int damage = Mathf.Max(Mathf.FloorToInt(baseAttack * multiplier) - effectiveDef, 1);
            
            CurrentBoss.CurrentHp = Mathf.Max(0, CurrentBoss.CurrentHp - damage);

            if (activeSkills.Count > 0)
            {
                AddLog($"【{string.Join(" + ", activeSkills)}】发动！造成 {damage} 伤害！");
            }
            else
            {
                AddLog($"反击！造成 {damage} 点伤害。");
            }
        }

        private void CrewAttack()
        {
            var crew = _crewSystem.GetActiveCrew();
            if (crew == null) return;

            int dps = _crewSystem.GetCurrentDPS();
            var cd = crew.NPCData.CombatData;
            
            bool isCrit = UnityEngine.Random.value < cd.CritChance;
            if (isCrit) dps = Mathf.FloorToInt(dps * cd.CritMultiplier);

            CurrentBoss.CurrentHp = Mathf.Max(0, CurrentBoss.CurrentHp - dps);
            CrewTotalDamage += dps;

            if (isCrit)
                AddLog($"💕 {crew.NPCData.Name} 暴击！造成 {dps} 伤害！");
            else
                AddLog($"💕 {crew.NPCData.Name} 攻击！造成 {dps} 伤害。");

            // 随机台词
            if (_playerData.Shame >= 30 && UnityEngine.Random.value < 0.3f)
            {
                var line = cd.PlayerShameLines[UnityEngine.Random.Range(0, cd.PlayerShameLines.Length)];
                AddLog($"💕 {crew.NPCData.Name}: \"{line}\"");
            }
        }

        private void UpdateShame()
        {
            int total = 0;
            foreach (Equipment.EquipmentSlot slot in Enum.GetValues(typeof(Equipment.EquipmentSlot)))
            {
                var item = _equipmentManager.GetEquipped(slot);
                if (item == null || !item.ContributesToShame) continue;
                
                int max = item.MaxDurability;
                int cur = _equipmentManager.CurrentDurability[slot];
                float ratio = max > 0 ? 1f - ((float)cur / max) : 0f;
                total += Mathf.FloorToInt(ratio * 33f * item.ShameWeight);
            }

            int oldShame = _playerData.Shame;
            _playerData.SetShame(Mathf.Min(total, _playerData.MaxShame));
            
            if (_playerData.Shame != oldShame)
            {
                AddLog($"😳 羞耻值: {oldShame} → {_playerData.Shame}");
                OnShameChanged?.Invoke(_playerData.Shame);
            }
        }

        private bool CheckPlayerDefeat()
        {
            // 所有外层衣服都损坏才算失败（内衣还在）
            var outerSlots = new[] { Equipment.EquipmentSlot.Top, Equipment.EquipmentSlot.Bottom };
            foreach (var slot in outerSlots)
            {
                var item = _equipmentManager.GetEquipped(slot);
                if (item != null && _equipmentManager.CurrentDurability[slot] > 0)
                    return false;
            }
            return true;
        }

        /// <summary>
        /// 结束战斗
        /// </summary>
        public void EndBattle(bool victory)
        {
            if (_battleCoroutine != null)
                StopCoroutine(_battleCoroutine);

            CurrentState = victory ? BattleState.Victory : BattleState.Defeat;

            if (victory)
            {
                AddLog("═══════════════════════════════");
                AddLog($"🎉 胜利！击败了 {CurrentBoss.BossName}！");
                
                // 奖励
                int goldReward = UnityEngine.Random.Range(CurrentBoss.MinGold, CurrentBoss.MaxGold + 1);
                int expReward = UnityEngine.Random.Range(CurrentBoss.MinExp, CurrentBoss.MaxExp + 1);
                _playerData.AddGold(goldReward);
                _playerData.AddExp(expReward);
                AddLog($"💰 +{goldReward}金币  ⭐ +{expReward}经验");

                // 掉落
                foreach (var drop in CurrentBoss.Drops)
                {
                    if (UnityEngine.Random.value <= drop.DropChance)
                    {
                        int count = UnityEngine.Random.Range(drop.MinCount, drop.MaxCount + 1);
                        AddLog($"📦 获得 {drop.ItemName} x{count}");
                    }
                }

                // NPC修补
                if (_crewSystem?.HasActiveCrew() == true)
                {
                    _crewSystem.RepairPlayerClothes();
                }
                
                // 战斗胜利后恢复全身立绘
                UpdateFullbodyAppearance();
            }
            else
            {
                AddLog("💀 你战败了...所有衣服都破损不堪...");
            }

            OnBattleEnded?.Invoke(victory);
        }

        /// <summary>
        /// 添加战斗日志
        /// </summary>
        public void AddLog(string message)
        {
            BattleLog.Add(message);
            if (BattleLog.Count > MaxLogEntries)
                BattleLog.RemoveAt(0);
            OnLogAdded?.Invoke(message);
        }

        /// <summary>
        /// 重置战斗
        /// </summary>
        public void ResetBattle()
        {
            if (_battleCoroutine != null)
                StopCoroutine(_battleCoroutine);
            CurrentState = BattleState.Idle;
            TurnCount = 0;
            CrewTotalDamage = 0;
            BattleLog.Clear();
            _playerData.SetShame(0);
            
            // 重置全身立绘为完整状态
            var appearance = _playerData?.GetComponent<Player.PlayerAppearance>();
            if (appearance != null && appearance.UseFullbodyMode)
                appearance.SetFullbodyStage(Equipment.DurabilityStage.Full);
        }

        /// <summary>
        /// 根据外层装备的最差耐久阶段，更新全身立绘
        /// </summary>
        private void UpdateFullbodyAppearance()
        {
            if (_playerData == null || _equipmentManager == null) return;

            var appearance = _playerData.GetComponent<Player.PlayerAppearance>();
            if (appearance == null || !appearance.UseFullbodyMode) return;

            // 检查外层装备（Top 和 Bottom）的最差耐久阶段
            var outerSlots = new[] { Equipment.EquipmentSlot.Top, Equipment.EquipmentSlot.Bottom };
            Equipment.DurabilityStage worstStage = Equipment.DurabilityStage.Full;

            foreach (var slot in outerSlots)
            {
                var item = _equipmentManager.GetEquipped(slot);
                if (item == null) continue;

                int current = _equipmentManager.CurrentDurability[slot];
                var stage = _equipmentManager.GetDurabilityStage(current, item.MaxDurability);
                if (stage > worstStage) worstStage = stage;
            }

            appearance.SetFullbodyStage(worstStage);
        }
    }

    public enum BattleState
    {
        Idle,
        Battling,
        Victory,
        Defeat
    }
}
